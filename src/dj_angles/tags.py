from collections.abc import Callable
from typing import TYPE_CHECKING, Optional, Union

from minestrone import Element

from dj_angles.attributes import Attributes
from dj_angles.caseconverter import kebabcase
from dj_angles.mappers.angles import map_angles_include
from dj_angles.settings import get_setting

if TYPE_CHECKING:
    from collections import deque


class Tag:
    """Encapsulates metadata and functionality for a tag that will be processed by `dj-angles`."""

    tag_name: str
    """The portion of the tag's element name after the initial identifier (which defaults to 'dj-').

    Examples:
        - 'include' for '<dj-include />'
        - 'partial' for '<dj-partial />'
    """

    html: str
    """The original HTML of the tag."""

    attributes: Attributes
    """The parsed attributes of the template tag."""

    is_shadow: bool = False
    """Whether or not the tag should use the Shadow DOM."""

    is_end: bool = False
    """Whether or not the tag is an end tag, i.e. starts with '</'."""

    is_self_closing: bool = False
    """Whether or not the tag is self-closing, i.e. ends with '/>'."""

    start_tag: Optional["Tag"] = None
    """The associated start tag. Only set for end tags."""

    def __init__(
        self,
        tag_map: Optional[dict[Optional[str], Union[Callable, str]]],
        html: str,
        tag_name: str,
        template_tag_args: str,
        tag_queue: Optional["deque"] = None,
    ):
        self.html = html
        self.tag_name = tag_name

        self._template_tag_args = template_tag_args
        self.parse_attributes()

        if self.tag_name.endswith("!"):
            self.tag_name = self.tag_name[:-1]
            self.is_shadow = True
        else:
            shadow_attribute = self.attributes.get("shadow")

            if shadow_attribute:
                self.is_shadow = True
                self.attributes.remove(shadow_attribute.key)

        if get_setting("lower_case_tag", default=False) is True:
            self.tag_name = self.tag_name.lower()

        if get_setting("slugify_tag", default=True) is True:
            self.tag_name = kebabcase(self.tag_name, strip_punctuation=False)

        if tag_map is None:
            raise AssertionError("Invalid tag_map")

        # Get the Django template tag based on the tag name or get the fallback with magic `None`
        self.django_template_tag = tag_map.get(self.tag_name) or tag_map.get(None)

        self.is_self_closing = self.html.endswith("/>")
        self.is_end = self.html.startswith("</")

        if self.is_end and tag_queue:
            # Assume that the last tag before this end tag was the related start tag
            self.start_tag = tag_queue[-1]

    def parse_attributes(self):
        """Creates `Attributes` based on the template tag arguments."""

        self.attributes = Attributes(self._template_tag_args)

    def get_django_template_tag(self, slots: Optional[list[tuple[str, Element]]] = None) -> str:
        """Generate the Django template tag.

        Args:
            param slots: List of slots which is a tuple of slot name and inner html.
        """

        if slots and self.is_include:
            self.django_template_tag = map_angles_include
            self.slots = slots

        if callable(self.django_template_tag):
            return str(
                self.django_template_tag(
                    tag=self,
                )
            )

        if self.is_end:
            self.django_template_tag = f"end{self.django_template_tag}"

        if self.attributes:
            return f"{{% {self.django_template_tag} {self.attributes} %}}"

        return f"{{% {self.django_template_tag} %}}"

    def get_wrapping_tag_name(self, name: Optional[str] = None) -> str:
        """Get the wrapping tag name.

        Args:
            param name: The name for the wrapping tag.
        """

        name = name or self.tag_name

        wrapping_tag_name = (
            name.replace("/", "-")
            .replace("'", "")
            .replace('"', "")
            .replace("--", "-")
            .replace(" ", "-")
            .replace(":", "-")
        ).lower()
        wrapping_tag_name = f"dj-{wrapping_tag_name}"

        # Remove extensions
        if "." in wrapping_tag_name:
            extension_idx = wrapping_tag_name.index(".")
            wrapping_tag_name = wrapping_tag_name[0:extension_idx]

        # Remove shadow bang
        if wrapping_tag_name.endswith("!"):
            wrapping_tag_name = wrapping_tag_name[:-1]

        return wrapping_tag_name

    @property
    def is_include(self):
        """Whether the Django template tag is `include`."""

        return callable(self.django_template_tag) and self.django_template_tag.__name__ == "map_include"

    @property
    def component_name(self):
        """Legacy property for `tag_name`. Deprecated."""

        return self.tag_name

    def __str__(self):
        return self.html
