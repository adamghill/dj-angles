import re
from typing import TYPE_CHECKING, Optional, cast

from django.conf import settings
from minestrone import Element

from dj_angles.attributes import Attributes
from dj_angles.caseconverter import kebabify
from dj_angles.exceptions import MissingAttributeError
from dj_angles.htmls import VOID_ELEMENTS
from dj_angles.mappers.angles import map_angles_include
from dj_angles.mappers.mapper import TagMap, get_tag_map
from dj_angles.settings import get_setting
from dj_angles.strings import dequotify
from dj_angles.templates import get_template

if TYPE_CHECKING:
    from collections import deque


SHADOW_ATTRIBUTE_KEY = "shadow"
DEFAULT_ATTRIBUTE_KEY = "default"

ERROR_BOUNDARY_ATTRIBUTE_KEY = "error-boundary"
ERROR_BOUNDARY_TAG_NAMES = ["block"]


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

    is_wrapped: bool = True
    """Whether or not the tag is wrapped."""

    is_end: bool = False
    """Whether or not the tag is an end tag, i.e. starts with '</'."""

    is_self_closing: bool = False
    """Whether or not the tag is self-closing, i.e. ends with '/>'."""

    start_tag: Optional["Tag"] = None
    """The associated start tag. Only set for end tags."""

    outer_html: str | None = None
    """The outer HTML of the tag."""

    is_error_boundary: bool = False
    """Whether or not the tag should handle errors."""

    error_fallback: str | None = ""
    """What to display if there is an error. Can be a string or a template."""

    inner_html: str | None = None

    def __init__(
        self,
        tag_map: TagMap | dict | None = None,
        html: str = "",
        tag_name: str = "",
        template_tag_args: str = "",
        tag_queue: Optional["deque"] = None,
    ):
        self.html = html
        self.tag_name = tag_name

        self._template_tag_args = template_tag_args
        self.attributes = Attributes()
        self.parse_attributes()

        if self.tag_name.endswith("!"):
            self.tag_name = self.tag_name[:-1]
            self.is_shadow = True
        elif self.attributes:
            if self.attributes.has(SHADOW_ATTRIBUTE_KEY):
                self.is_shadow = True
                self.attributes.remove(SHADOW_ATTRIBUTE_KEY)

        if self.attributes.has("no-wrap"):
            self.is_wrapped = False
            self.attributes.remove("no-wrap")

        if self.tag_name == "error-boundary":
            self.is_error_boundary = True
        elif self.tag_name in ERROR_BOUNDARY_TAG_NAMES and self.attributes.has(ERROR_BOUNDARY_ATTRIBUTE_KEY):
            self.is_error_boundary = True
            self.attributes.remove(ERROR_BOUNDARY_ATTRIBUTE_KEY)

        if self.is_error_boundary:
            if attribute := self.attributes.get(DEFAULT_ATTRIBUTE_KEY):
                self.error_fallback = dequotify(attribute.value)
                self.attributes.remove(DEFAULT_ATTRIBUTE_KEY)

        if get_setting("lower_case_tag", default=False) is True:
            self.tag_name = self.tag_name.lower()

        if get_setting("kebab_case_tag", default=True) is True:
            self.tag_name = kebabify(self.tag_name, strip_punctuation=False)

        if tag_map is None:
            tag_map = get_tag_map()

        # Get the Django template tag based on the tag name or get the fallback with magic `None`
        self.django_template_tag = tag_map.get(self.tag_name) or tag_map.get(None)

        self.is_self_closing = self.html.endswith("/>")
        self.is_end = self.html.startswith("</")

        if self.is_end and tag_queue:
            # Assume that the last tag before this end tag was the related start tag
            self.start_tag = tag_queue[-1]

    def parse_attributes(self):
        """Creates `Attributes` based on the template tag arguments."""

        # print("self._template_tag_args", self._template_tag_args)
        self.attributes = Attributes(self._template_tag_args)

        if self.is_shadow and self.attributes.has(SHADOW_ATTRIBUTE_KEY):
            self.attributes.remove(SHADOW_ATTRIBUTE_KEY)

    def get_error_html(self, exception: Exception) -> str:
        """Get HTML for the tag when there is an error."""

        if self.error_fallback:
            if fallback_template := get_template(self.error_fallback, raise_exception=False):
                return fallback_template.render({})

            return self.error_fallback

        html = ""

        if hasattr(exception, "template_debug"):
            template_debug = cast(dict, exception.template_debug)
            source = template_debug["name"]

            if hasattr(settings, "BASE_DIR"):
                original_source = source
                source = source.replace(str(settings.BASE_DIR), "")

                if original_source != source and source.startswith("/"):
                    source = source[1:]

            during = template_debug["during"]
            during = during.replace("{", "&#123;").replace("}", "&#125;")
            during = f"<pre><code>{{% verbatim %}}{during}{{% endverbatim %}}</code></pre>"

            if source == "<unknown source>":
                html = f"""<h2>
  {template_debug["message"]}
</h2>
<p>
  {during}
</p>"""
            else:
                error = template_debug["message"]

                if hasattr(exception, "tried"):
                    error = f"Could not find the template: '{error}'"

                    if exception.tried:
                        error = f"{error}: {', '.join(cast(list[str], exception.tried))}"

                if not error.endswith("."):
                    error = f"{error}."

                html = f"""<h2>
  {source}
</h2>
<p>
  <em>{error}</em>
</p>
<p>
  {during}
</p>
"""
        else:
            html = f"<em>{exception}</em>"

        error_style = get_setting(
            key_path="error_boundaries",
            setting_name="style",
            default="border: 1px red solid; padding: 0 24px 0 24px;",
        )
        error_class = get_setting(key_path="error_boundaries", setting_name="class", default="")

        html = f"<div style='{error_style}' class='{error_class}'>{html}</div>"

        if get_setting(key_path="error_boundaries", setting_name="shadow", default=True):
            html = f'<div><template shadowrootmode="open">{html}</template></div>'

        return html

    def get_django_template_tag(self, slots: list[tuple[str, Element]] | None = None) -> str:
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

    def get_wrapping_tag_name(self, name: str | None = None) -> str:
        """Get the wrapping tag name.

        Args:
            param name: The name for the wrapping tag.
        """

        name = name or self.tag_name

        # Remove quotes
        name = name.replace("'", "").replace('"', "")

        # Replace separators with hyphens
        name = re.sub(r"[/: ]+", "-", name)

        # Collapse multiple hyphens
        name = re.sub(r"-+", "-", name)

        wrapping_tag_name = f"dj-{name.lower()}"

        # Remove extensions
        if "." in wrapping_tag_name:
            extension_idx = wrapping_tag_name.index(".")
            wrapping_tag_name = wrapping_tag_name[0:extension_idx]

        # Remove shadow bang
        if wrapping_tag_name.endswith("!"):
            wrapping_tag_name = wrapping_tag_name[:-1]

        return wrapping_tag_name

    def pop_attribute_value_or_first_key(self, attribute_name: str) -> str:
        """Gets the first attribute key or the first value for a particular attribute name.

        As a side effect of this function, if the attribute is found, it will be removed from
        `tag.attributes` because almost always that is the desired behavior. `tag.parse_attributes()`
        can be called for the `tag` if needed for future needs, i.e. when in an end tag and needing
        the attributes for a start tag.

        Args:
            param attribute_name: The name of the attribute to get.
        """

        attr = self.attributes.get(attribute_name)

        if attr:
            self.attributes.remove(attribute_name)

            return attr.value or ""

        try:
            attr = self.attributes.pop(0)
        except IndexError as err:
            raise MissingAttributeError(attribute_name) from err

        val = None

        if not attr.has_value:
            val = attr.key

        if not val:
            raise MissingAttributeError(attribute_name)

        return val

    @property
    def is_include(self):
        """Whether the Django template tag is `include`."""

        return (
            callable(self.django_template_tag) and getattr(self.django_template_tag, "__name__", None) == "map_include"
        )

    @property
    def can_be_void(self):
        """Whether the tag can be a void element."""

        return self.tag_name in VOID_ELEMENTS

    @property
    def component_name(self):
        """Legacy property for `tag_name`. Deprecated."""

        return self.tag_name

    def __str__(self):
        return self.html
