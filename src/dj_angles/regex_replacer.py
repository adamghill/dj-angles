import re
from collections import deque
from functools import lru_cache
from typing import Any, List, Tuple

from dj_angles.exceptions import InvalidEndTagError
from dj_angles.mappers import HTML_TAG_TO_DJANGO_TEMPLATE_TAG_MAP, Tag
from dj_angles.settings import get_setting


def _get_tag_regex():
    initial_tag_regex = get_setting("initial_tag_regex", default=r"(dj-)")

    if initial_tag_regex is None:
        initial_tag_regex = ""

    tag_regex = rf"</?({initial_tag_regex}(?P<component_name>[^\s>]+))\s*(?P<template_tag_args>.*?)\s*/?>"

    @lru_cache(maxsize=32)
    def _compile_regex(_tag_regex):
        return re.compile(_tag_regex)

    return _compile_regex(tag_regex)


def get_replacements(html: str, *, raise_for_missing_start_tag: bool = True) -> List[Tuple[str, Any]]:
    replacements = []
    tag_regex = _get_tag_regex()
    tag_queue = deque()

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
    replacements = get_replacements(html=html)

    for r in replacements:
        html = html.replace(
            r[0],
            r[1],
        )

    return html
