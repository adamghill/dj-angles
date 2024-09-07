import re
from functools import lru_cache
from typing import Any, List, Tuple

from dj_angles.mappers import HTML_TAG_TO_DJANGO_TEMPLATE_TAG_MAP, map_include
from dj_angles.settings import get_setting
from dj_angles.wrapper import get_wrapping_element_name


def _get_tag_regex():
    initial_tag_regex = get_setting("initial_tag_regex", default=r"(dj-)")

    if initial_tag_regex is None:
        initial_tag_regex = ""

    tag_regex = rf"</?({initial_tag_regex}(?P<component_name>[^\s>]+))\s*(?P<template_tag_args>.*?)\s*/?>"

    @lru_cache(maxsize=32)
    def _compile_regex(_tag_regex):
        return re.compile(_tag_regex)

    return _compile_regex(tag_regex)


def get_replacements(template_string: str) -> List[Tuple[str, Any]]:
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

        if get_setting("lower_case_tag", default=False):
            component_name = component_name.lower()

        replacement = None
        is_tag_closing = original.startswith("</")
        is_tag_self_closing = original.endswith("/>")

        tag_map = HTML_TAG_TO_DJANGO_TEMPLATE_TAG_MAP
        tag_map.update(get_setting("mappers", default={}))

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
                    component_name=component_name,
                    template_tag_args=template_tag_args,
                    is_tag_closing=is_tag_closing,
                    is_tag_self_closing=is_tag_self_closing,
                )
            elif template_tag_args:
                replacement = f"{{% {django_template_tag} {template_tag_args} %}}"
            else:
                replacement = f"{{% {django_template_tag} %}}"
        elif original.startswith("</"):
            wrapping_element_name = get_wrapping_element_name(component_name)
            replacement = f"</template></{wrapping_element_name}>"
        else:
            # Handle `include` shorthand, e.g. `<dj-partial />` or `<partial />`
            template_tag_args = component_name

            # Handle shadow shorthand
            if component_name.endswith("!"):
                template_tag_args = component_name[:-1]
                template_tag_args += " shadow "

            template_tag_args += match.group("template_tag_args") or ""

            if not is_tag_self_closing:
                last_open_component_name = component_name

            replacement = map_include(
                component_name=component_name,
                template_tag_args=template_tag_args,
                is_tag_self_closing=is_tag_self_closing,
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
