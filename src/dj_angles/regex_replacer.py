import re
from collections import deque
from functools import lru_cache
from importlib.util import find_spec

from minestrone import HTML

from dj_angles.exceptions import InvalidEndTagError
from dj_angles.mappers.django import map_autoescape, map_block, map_css, map_extends, map_image, map_include
from dj_angles.mappers.thirdparty import map_bird
from dj_angles.settings import get_setting
from dj_angles.tags import Tag

HTML_TAG_TO_DJANGO_TEMPLATE_TAG_MAP = {
    "extends": map_extends,
    "block": map_block,
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
    "image": map_image,
    "css": map_css,
}
"""Default mappings for tags to Django template tags."""

tag_map: dict = None


def _is_module_available(module_name):
    return find_spec(module_name) is not None


def _get_tag_regex():
    """Gets a compiled regex based on the `initial_tag_regex` setting or default of r'(dj-)'."""

    initial_tag_regex = get_setting("initial_tag_regex", default=r"(dj-)")

    if initial_tag_regex is None:
        initial_tag_regex = ""

    tag_regex = rf"</?({initial_tag_regex}(?P<component_name>[^\s>]+))\s*(?P<template_tag_args>.*?)\s*/?>"

    @lru_cache(maxsize=32)
    def _compile_regex(_tag_regex):
        """Silly internal function to cache the compiled regex."""

        return re.compile(_tag_regex)

    return _compile_regex(tag_regex)


def get_tag_map() -> dict:
    """Get the complete tag map based on the default, dynamic, and settings mappers."""

    global tag_map  # noqa: PLW0603

    if tag_map is None:
        tag_map = HTML_TAG_TO_DJANGO_TEMPLATE_TAG_MAP

        if _is_module_available("django_bird"):
            tag_map.update({"bird": map_bird})

        tag_map.update(get_setting("mappers", default={}))

    return tag_map


def clear_tag_map() -> None:
    """Clear the generated tag map so that it will be re-generated. Useful for tests."""

    global tag_map  # noqa: PLW0603
    tag_map = None


def get_replacements(html: str, *, raise_for_missing_start_tag: bool = True) -> list[tuple[str, str]]:
    """Get a list of replacements (tuples that consists of 2 strings) based on the template HTML.

    Args:
        param html: Template HTML.
        param raise_for_missing_start_tag: Whether or not to raise an error if an invalid tag is discovered.

    Returns:
        A list of tuples where the first item in the tuple is the existing tag element, e.g. "<dj-csrf />"
        and the second item is the replacement string, e.g. "{% csrf_token %}".
    """

    replacements = []
    tag_regex = _get_tag_regex()
    tag_queue: deque = deque()

    tag_map = get_tag_map()

    for match in re.finditer(tag_regex, html):
        tag_html = html[match.start() : match.end()].strip()
        component_name = match.group("component_name").strip()
        template_tag_args = match.group("template_tag_args").strip()

        tag = Tag(tag_map=tag_map, html=tag_html, component_name=component_name, template_tag_args=template_tag_args)

        if raise_for_missing_start_tag:
            if tag.is_end:
                _last_tag: Tag = tag_queue.pop()

                if _last_tag.component_name != tag.component_name:
                    raise InvalidEndTagError(tag=tag, last_tag=_last_tag)
            elif not tag.is_self_closing:
                tag_queue.append(tag)

        slots = []

        # Parse the inner HTML for includes to handle slots
        # TODO: Check settings to see if slots are enabled
        if (
            get_setting("SLOTS_ENABLED", default=False)
            and not tag.is_self_closing
            and not tag.is_end
            and (
                tag.django_template_tag is None
                or (callable(tag.django_template_tag) and tag.django_template_tag.__name__ == "map_include")
            )
        ):
            end_of_include_tag = match.end()

            try:
                # TODO: handle custom tag, not just /dj-
                next_ending_tag_idx = html.index("</dj-", end_of_include_tag)
                inner_html = html[end_of_include_tag:next_ending_tag_idx].strip()

                if inner_html:
                    for element in HTML(inner_html).elements:
                        if slot_name := element.attributes.get("slot"):
                            slots.append((slot_name, element))

                            # Remove slot from the current HTML because it will be injected into the include component
                            replacements.append((inner_html, ""))
            except ValueError:
                # Ending tag could not be found, so skip getting the inner html
                pass

        django_template_tag = tag.get_django_template_tag(slots=slots)

        if django_template_tag:
            replacements.append((tag.html, django_template_tag))

    return replacements


def replace_django_template_tags(html: str) -> str:
    """Gets a list of replacements based on template HTML, replaces the necessary strings, and returns the new string.

    Args:
        param html: Template HTML.

    Returns:
        The converted template HTML.
    """

    replacements = get_replacements(html=html)

    for r in replacements:
        html = html.replace(
            r[0],
            r[1],
        )

    return html
