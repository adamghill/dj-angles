from dataclasses import dataclass

from dj_angles.settings import get_setting


@dataclass
class Tag:
    """Encapsulates metadata and functionality for a tag that will be processed by `dj-angles`."""

    """The tag name after the initial identifier (which defaults to 'dj-').

    Examples:
        - 'include' for '<dj-include />'
        - 'partial' for '<dj-partial />'
    """
    component_name: str

    tag_html: str

    """The arguments passed into the template tag.

    Examples:
        - '"partial.html"' for '<dj-include "partial.html" />'
    """
    template_tag_args: str

    """Whether or not the tag should use the Shadow DOM.
    """
    is_shadow: bool = False

    """Whether or not the tag is an end tag, i.e. starts with '</'.
    """
    is_end: bool = False

    """Whether or not the tag is self-closing, i.e. ends with '/>'.
    """
    is_self_closing: bool = False

    def __init__(self, tag_map: dict, html: str, component_name: str, template_tag_args: str):
        """Constructor which takes in a dictionary of the available tags, the tag html,
        the component name, and the template tag arguments.
        """

        self.html = html
        self.component_name = component_name
        self.template_tag_args = template_tag_args

        if self.component_name.endswith("!"):
            self.component_name = self.component_name[:-1]
            self.is_shadow = True
        else:
            _template_tag_args = ""

            for template_tag_arg in self.template_tag_args.split(" "):
                if template_tag_arg.strip() == "shadow":
                    self.is_shadow = True
                else:
                    _template_tag_args += f"{template_tag_arg} "

            self.template_tag_args = _template_tag_args.strip()

        if get_setting("lower_case_tag", default=False):
            self.component_name = self.component_name.lower()

        self.is_end = self.html.startswith("</")
        self.is_self_closing = self.html.endswith("/>")

        self.django_template_tag = tag_map.get(self.component_name)

    def get_django_template_tag(self) -> str:
        if self.django_template_tag is None and self.is_end:
            wrapping_tag_name = self.get_wrapping_tag_name()

            return f"</template></{wrapping_tag_name}>"

        if self.django_template_tag is None:
            # Assume any missing template tag is an include
            self.django_template_tag = map_include
            self.template_tag_args = f"{self.component_name} {self.template_tag_args}"

        if callable(self.django_template_tag):
            return self.django_template_tag(
                tag=self,
            )

        if self.is_end:
            self.django_template_tag = f"end{self.django_template_tag}"

        if self.template_tag_args:
            return f"{{% {self.django_template_tag} {self.template_tag_args} %}}"

        return f"{{% {self.django_template_tag} %}}"

    def get_wrapping_tag_name(self, name=None) -> str:
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


def map_autoescape(tag: Tag) -> str:
    """Mapper function for the autoescape tags."""

    django_template_tag = tag.component_name

    if tag.is_end:
        django_template_tag = django_template_tag[0:10]
        django_template_tag = f"end{django_template_tag}"
    else:
        django_template_tag = django_template_tag.replace("-", " ")

    return f"{{% {django_template_tag} %}}"


def map_include(tag: Tag) -> str:
    if not tag.template_tag_args:
        raise AssertionError("{% include %} must have an template name")

    template_file = tag.template_tag_args.split(" ")[0]
    tag.template_tag_args = " ".join(tag.template_tag_args.split(" ")[1:])

    is_double_quoted = False

    if template_file.startswith("'") and template_file.endswith("'"):
        template_file = template_file[1:-1]
    elif template_file.startswith('"') and template_file.endswith('"'):
        template_file = template_file[1:-1]
        is_double_quoted = True

    if "." not in template_file:
        template_file = f"{template_file}.html"

    if is_double_quoted:
        template_file = f'"{template_file}"'
    else:
        template_file = f"'{template_file}'"

    wrapping_tag_name = tag.get_wrapping_tag_name(name=template_file)

    if ":" in template_file:
        colon_idx = template_file.index(":")
        extension_idx = template_file.index(".")
        template_file = template_file[0:colon_idx] + template_file[extension_idx:]

    replacement = ""

    if tag.template_tag_args:
        replacement = f"{{% include {template_file} {tag.template_tag_args} %}}"
    else:
        replacement = f"{{% include {template_file} %}}"

    if tag.is_shadow:
        replacement = f"<{wrapping_tag_name}><template shadowrootmode='open'>{replacement}"

        if tag.is_self_closing:
            replacement = f"{replacement}</template></{wrapping_tag_name}>"
    else:
        replacement = f"<{wrapping_tag_name}>{replacement}"

        if tag.is_self_closing:
            replacement = f"{replacement}</{wrapping_tag_name}>"

    return replacement


# Default mappings for tag names to Django template tags
HTML_TAG_TO_DJANGO_TEMPLATE_TAG_MAP = {
    "extends": "extends",
    "block": "block",
    "verbatim": "verbatim",
    "include": map_include,
    "comment": "comment",
    "#": "comment",
    "autoescape-on": map_autoescape,
    "autoescape-off": map_autoescape,
    "csrf-token": "csrf_token",
    "csrf": "csrf_token",
    "csrf-input": "csrf_token",
    "debug": "debug",
    "filter": "filter",
    "lorem": "lorem",
    "now": "now",
    "spaceless": "spaceless",
    "templatetag": "templatetag",
}
