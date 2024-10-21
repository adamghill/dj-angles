from typing import TYPE_CHECKING, Optional

from minestrone import Element

from django.utils.module_loading import import_string

from dj_angles.attributes import Attributes
from dj_angles.mappers.angles import map_angles_include
from dj_angles.settings import get_setting

if TYPE_CHECKING:
    from collections import deque


class Tag:
    """Encapsulates metadata and functionality for a tag that will be processed by `dj-angles`."""

    component_name: str
    """The tag name after the initial identifier (which defaults to 'dj-').

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

    start_tag: "Tag" = None
    """The associated start tag. Only set for end tags."""

    def __init__(
        self, tag_map: dict, html: str, component_name: str, template_tag_args: str, tag_queue: Optional["deque"] = None
    ):
        self.html = html
        self.component_name = component_name

        self._template_tag_args = template_tag_args
        self.parse_attributes()

        if self.component_name.endswith("!"):
            self.component_name = self.component_name[:-1]
            self.is_shadow = True
        else:
            shadow_attribute = self.attributes.get("shadow")

            if shadow_attribute:
                self.is_shadow = True
                self.attributes.remove(shadow_attribute.key)

        if get_setting("lower_case_tag", default=False):
            self.component_name = self.component_name.lower()

        self.django_template_tag = tag_map.get(self.component_name)

        self.is_self_closing = self.html.endswith("/>")
        self.is_end = self.html.startswith("</")

        if self.is_end and tag_queue:
            # Assume that the last tag before this end tag was the related start tag
            self.start_tag = tag_queue[-1]

    def parse_attributes(self):
        self.attributes = Attributes(self._template_tag_args)

    def get_django_template_tag(self, slots: Optional[list[tuple[str, Element]]] = None) -> str:
        """Generate the Django template tag.

        Args:
            param slots: List of slots which is a tuple of slot name and inner html.
        """

        if self.django_template_tag is None and self.is_end:
            wrapping_tag_name = self.get_wrapping_tag_name()

            django_template_tag = ""

            if self.is_shadow or (self.start_tag and self.start_tag.is_shadow):
                django_template_tag = "</template>"

            return f"{django_template_tag}</{wrapping_tag_name}>"

        if self.django_template_tag is None:
            # Assume any missing template tag should use the fallback mapper
            self.django_template_tag = import_string(
                get_setting("default_component_mapper", "dj_angles.mappers.include.map_include")
            )

            # Add component name to the template tags
            self.attributes.prepend(self.component_name)

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

        name = name or self.component_name

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
        return callable(self.django_template_tag) and self.django_template_tag.__name__ == "map_include"

    def __str__(self):
        return self.html
