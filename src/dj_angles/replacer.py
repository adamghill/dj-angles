import re
from functools import lru_cache

from django.conf import settings

from dj_angles.mappers import HTML_TAG_TO_DJANGO_TEMPLATE_TAG_MAP


def get_include_replacement(template_name: str, *, is_shadow: bool = False, is_tag_self_closing: bool = False) -> str:
    template_file = template_name.strip()
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

    replacement = f"{{% include {template_file} %}}"

    if is_shadow:
        replacement = f"<template shadowrootmode='open'>{{% include {template_file} %}}"

        if is_tag_self_closing:
            replacement = f"{replacement}</template>"

    return replacement


def _get_setting(setting_name: str, no_setting_default=None, default=None):
    if not hasattr(settings, "ANGLES"):
        settings.ANGLES = {}

    if setting_name in settings.ANGLES:
        return settings.ANGLES[setting_name] or default

    return no_setting_default


def _get_tag_regex():
    initial_tag_regex = _get_setting("initial_tag_regex", no_setting_default=r"(dj-)", default="")
    tag_regex = rf"</?({initial_tag_regex}(?P<component_name>[^\s>]+))\s*(?P<template_tag_args>.*?)\s*/?>"

    @lru_cache(maxsize=32)
    def _compile_regex(_tag_regex):
        return re.compile(_tag_regex)

    return _compile_regex(tag_regex)


def get_replacements(template_string: str) -> list[str]:
    replacements = []
    last_open_component_name = None

    tag_regex = _get_tag_regex()

    for match in re.finditer(tag_regex, template_string):
        original = template_string[match.start() : match.end()]
        component_name = match.group("component_name").strip()

        if last_open_component_name:
            if component_name.endswith("!"):
                if last_open_component_name != component_name[:-1]:
                    raise AssertionError(f"Expected closing tag for {component_name[:-1]}")
            elif last_open_component_name != component_name:
                raise AssertionError(f"Expected closing tag for {component_name}")

            last_open_component_name = None

        if _get_setting("lower_case_tag", no_setting_default=False, default=False):
            component_name = component_name.lower()

        replacement = None
        is_tag_closing = original.startswith("</")
        is_tag_self_closing = original.endswith("/>")

        tag_map = HTML_TAG_TO_DJANGO_TEMPLATE_TAG_MAP
        tag_map.update(_get_setting("mappers", no_setting_default={}, default={}))

        if django_template_tag := tag_map.get(component_name):
            # Get a string of the rest of the match after the component name
            # TODO: Parse template_tag_args to be able to handle more complicated cases?
            template_tag_args: str = match.group("template_tag_args")

            is_django_template_tag_callable = callable(django_template_tag)

            # Handle end tags
            if is_tag_closing and not is_django_template_tag_callable:
                django_template_tag = f"end{django_template_tag}"

            if is_django_template_tag_callable:
                replacement = django_template_tag(
                    component_name=component_name, template_tag_args=template_tag_args, is_tag_closing=is_tag_closing
                )
            elif django_template_tag == "include":
                is_shadow = False

                if "shadow" in template_tag_args:
                    # Remove shadow from the arg if necessary
                    template_tag_args = template_tag_args.replace("shadow", "")
                    is_shadow = True

                if not template_tag_args:
                    raise AssertionError("{% include %} must have an template name")

                replacement = get_include_replacement(
                    template_name=template_tag_args, is_shadow=is_shadow, is_tag_self_closing=is_tag_self_closing
                )
            elif template_tag_args:
                replacement = f"{{% {django_template_tag} {template_tag_args} %}}"
            else:
                replacement = f"{{% {django_template_tag} %}}"
        elif original.startswith("</"):
            replacement = "</template>"
        else:
            # Handle `include` shorthand, e.g. `<dj-partial />` or `<partial />`
            is_shadow = "shadow" in match.group("template_tag_args")

            if component_name.endswith("!"):
                # Handle shadow shorthand
                component_name = component_name[:-1]
                is_shadow = True

            if not is_tag_self_closing:
                last_open_component_name = component_name

            replacement = get_include_replacement(
                template_name=component_name, is_shadow=is_shadow, is_tag_self_closing=is_tag_self_closing
            )

        if replacement:
            replacements.append((original, replacement))

    return replacements


def replace_django_templatetags(template_string: str) -> str:
    replacements = get_replacements(template_string=template_string)

    for r in replacements:
        template_string = template_string.replace(
            r[0],
            r[1],
        )

    return template_string
