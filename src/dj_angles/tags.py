from typing import Optional

from dj_angles.attributes import Attributes
from dj_angles.mappers import map_include
from dj_angles.settings import get_setting


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

    def __init__(self, tag_map: dict, html: str, component_name: str, template_tag_args: str):
        self.html = html
        self.component_name = component_name

        self._template_tag_args = template_tag_args

        self.attributes = Attributes(self._template_tag_args)

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

        self.is_end = self.html.startswith("</")
        self.is_self_closing = self.html.endswith("/>")

        self.django_template_tag = tag_map.get(self.component_name)

    def get_django_template_tag(self) -> str:
        """Generate the Django template tag."""

        if self.django_template_tag is None and self.is_end:
            wrapping_tag_name = self.get_wrapping_tag_name()

            return f"</template></{wrapping_tag_name}>"

        if self.django_template_tag is None:
            # Assume any missing template tag is an include
            self.django_template_tag = map_include

            # Add component name to the template tags
            self.attributes.prepend(self.component_name)

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

    def __str__(self):
        return self.html
