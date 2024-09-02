def get_autoescape(*, component_name: str, is_tag_closing: bool = False, **kwargs) -> str:
    django_template_tag = component_name

    if is_tag_closing:
        django_template_tag = django_template_tag[0:10]
        django_template_tag = f"end{django_template_tag}"
    else:
        django_template_tag = django_template_tag.replace("-", " ")

    return f"{{% {django_template_tag} %}}"


HTML_TAG_TO_DJANGO_TEMPLATE_TAG_MAP = {
    "extends": "extends",
    "block": "block",
    "verbatim": "verbatim",
    "include": "include",
    "$": "include",  # technically not needed, but more explicit
    "comment": "comment",
    "#": "comment",
    "autoescape-on": get_autoescape,
    "autoescape-off": get_autoescape,
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
