from dj_angles.wrapper import get_wrapping_element_name


def map_autoescape(*, component_name: str, is_tag_closing: bool = False, **kwargs) -> str:  # noqa: ARG001
    """Mapper function for the autoescape tags."""

    django_template_tag = component_name

    if is_tag_closing:
        django_template_tag = django_template_tag[0:10]
        django_template_tag = f"end{django_template_tag}"
    else:
        django_template_tag = django_template_tag.replace("-", " ")

    return f"{{% {django_template_tag} %}}"


def map_include(*, template_tag_args: str, is_tag_self_closing: bool, **kwargs) -> str:  # noqa: ARG001
    is_shadow = False

    _template_tag_args = ""

    for template_tag_arg in template_tag_args.split(" "):
        if template_tag_arg.strip() == "shadow":
            is_shadow = True
        else:
            _template_tag_args += f"{template_tag_arg} "

    template_tag_args = _template_tag_args.strip()

    if not template_tag_args:
        raise AssertionError("{% include %} must have an template name")

    template_file = template_tag_args

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

    wrapping_element_name = get_wrapping_element_name(template_file)

    if ":" in template_file:
        colon_idx = template_file.index(":")
        extension_idx = template_file.index(".")
        template_file = template_file[0:colon_idx] + template_file[extension_idx:]

    replacement = f"{{% include {template_file} %}}"

    if is_shadow:
        replacement = f"<{wrapping_element_name}><template shadowrootmode='open'>{{% include {template_file} %}}"

        if is_tag_self_closing:
            replacement = f"{replacement}</template></{wrapping_element_name}>"
    else:
        replacement = f"<{wrapping_element_name}>{replacement}"

        if is_tag_self_closing:
            replacement = f"{replacement}</{wrapping_element_name}>"

    return replacement


# Defaults mappings for tag names to Django template tags
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
