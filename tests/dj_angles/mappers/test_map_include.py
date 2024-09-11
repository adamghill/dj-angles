import re

from dj_angles.mappers import map_include
from dj_angles.regex_replacer import HTML_TAG_TO_DJANGO_TEMPLATE_TAG_MAP, _get_tag_regex
from dj_angles.tags import Tag


def _get_match(html: str):
    tag_regex = _get_tag_regex()
    return re.match(tag_regex, html)


def _get_tag(html: str):
    match = _get_match(html)
    tag_html = html[match.start() : match.end()]
    component_name = match.group("component_name").strip()
    template_tag_args = match.group("template_tag_args").strip()

    return Tag(
        HTML_TAG_TO_DJANGO_TEMPLATE_TAG_MAP,
        html=tag_html,
        component_name=component_name,
        template_tag_args=template_tag_args,
    )


def test_not_self_closing():
    expected = "<dj-partial>{% include 'partial.html' %}"

    html = "<dj-include 'partial'>"
    tag = _get_tag(html)

    actual = map_include(tag=tag)

    assert actual == expected


def test_no_extension():
    expected = "<dj-partial>{% include 'partial.html' %}</dj-partial>"

    html = "<dj-include 'partial' />"
    tag = _get_tag(html)

    actual = map_include(tag=tag)

    assert actual == expected


def test_single_quotes():
    expected = "<dj-partial>{% include 'partial.html' %}</dj-partial>"

    html = "<dj-include 'partial.html' />"
    tag = _get_tag(html)

    actual = map_include(tag=tag)

    assert actual == expected


def test_double_quotes():
    expected = '<dj-partial>{% include "partial.html" %}</dj-partial>'

    html = '<dj-include "partial.html" />'
    tag = _get_tag(html)

    actual = map_include(tag=tag)

    assert actual == expected


def test_extension():
    expected = "<dj-partial>{% include 'partial.html' %}</dj-partial>"

    html = "<dj-include 'partial.html' />"
    tag = _get_tag(html)

    actual = map_include(tag=tag)

    assert actual == expected


def test_directory():
    expected = "<dj-more-partial>{% include 'more/partial.html' %}</dj-more-partial>"

    html = "<dj-include 'more/partial' />"
    tag = _get_tag(html)

    actual = map_include(tag=tag)

    assert actual == expected


def test_shadow():
    expected = "<dj-partial><template shadowrootmode='open'>{% include 'partial.html' %}</template></dj-partial>"

    html = "<dj-include 'partial.html' shadow />"
    tag = _get_tag(html)

    actual = map_include(tag=tag)

    assert actual == expected
