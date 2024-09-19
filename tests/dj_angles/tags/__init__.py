import re

from dj_angles.regex_replacer import HTML_TAG_TO_DJANGO_TEMPLATE_TAG_MAP, _get_tag_regex
from dj_angles.tags import Tag


def create_tag(html):
    tag_regex = _get_tag_regex()
    match = re.match(tag_regex, html)

    tag_html = html[match.start() : match.end()]
    component_name = match.group("component_name").strip()
    template_tag_args = match.group("template_tag_args").strip()

    return Tag(
        HTML_TAG_TO_DJANGO_TEMPLATE_TAG_MAP,
        html=tag_html,
        component_name=component_name,
        template_tag_args=template_tag_args,
    )
