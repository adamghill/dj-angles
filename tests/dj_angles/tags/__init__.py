import re

from dj_angles.regex_replacer import _get_tag_regex, get_tag_map
from dj_angles.tags import Tag


def create_tag(html):
    tag_regex = _get_tag_regex()
    match = re.match(tag_regex, html)

    tag_html = html[match.start() : match.end()]
    tag_name = match.group("tag_name").strip()
    template_tag_args = match.group("template_tag_args").strip()

    tag_map = get_tag_map()

    return Tag(
        tag_map,
        html=tag_html,
        tag_name=tag_name,
        template_tag_args=template_tag_args,
    )
