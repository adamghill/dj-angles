import re
from collections import deque
from functools import lru_cache
from typing import List, Tuple

from dj_angles.exceptions import InvalidEndTagError
from dj_angles.mappers import map_autoescape, map_css, map_image, map_include
from dj_angles.settings import get_setting
from dj_angles.tags import Tag

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
    "image": map_image,
    "css": map_css,
}
"""Default mappings for tags to Django template tags."""


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


def get_replacements(html: str, *, raise_for_missing_start_tag: bool = True) -> List[Tuple[str, str]]:
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

    tag_map = HTML_TAG_TO_DJANGO_TEMPLATE_TAG_MAP
    tag_map.update(get_setting("mappers", default={}))

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

        django_template_tag = tag.get_django_template_tag()

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
