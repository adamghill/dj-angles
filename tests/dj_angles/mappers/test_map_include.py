import re

from dj_angles.mappers import HTML_TAG_TO_DJANGO_TEMPLATE_TAG_MAP, Tag, map_include
from dj_angles.replacer import _get_tag_regex


def _get_match(html: str):
    tag_regex = _get_tag_regex()
    return re.match(tag_regex, html)


def _get_tag(html: str):
    match = _get_match(html)

    return Tag(HTML_TAG_TO_DJANGO_TEMPLATE_TAG_MAP, html, match=match)


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
