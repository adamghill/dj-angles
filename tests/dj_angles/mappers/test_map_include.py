from dj_angles.mappers import map_include
from tests.dj_angles.tags import create_tag


def test_not_self_closing():
    expected = "<dj-partial>{% include 'partial.html' %}"

    html = "<dj-include 'partial'>"
    tag = create_tag(html)

    actual = map_include(tag=tag)

    assert actual == expected


def test_no_extension():
    expected = "<dj-partial>{% include 'partial.html' %}</dj-partial>"

    html = "<dj-include 'partial' />"
    tag = create_tag(html)

    actual = map_include(tag=tag)

    assert actual == expected


def test_single_quotes():
    expected = "<dj-partial>{% include 'partial.html' %}</dj-partial>"

    html = "<dj-include 'partial.html' />"
    tag = create_tag(html)

    actual = map_include(tag=tag)

    assert actual == expected


def test_double_quotes():
    expected = '<dj-partial>{% include "partial.html" %}</dj-partial>'

    html = '<dj-include "partial.html" />'
    tag = create_tag(html)

    actual = map_include(tag=tag)

    assert actual == expected


def test_extension():
    expected = "<dj-partial>{% include 'partial.html' %}</dj-partial>"

    html = "<dj-include 'partial.html' />"
    tag = create_tag(html)

    actual = map_include(tag=tag)

    assert actual == expected


def test_directory():
    expected = "<dj-more-partial>{% include 'more/partial.html' %}</dj-more-partial>"

    html = "<dj-include 'more/partial' />"
    tag = create_tag(html)

    actual = map_include(tag=tag)

    assert actual == expected


def test_shadow():
    expected = "<dj-partial><template shadowrootmode='open'>{% include 'partial.html' %}</template></dj-partial>"

    html = "<dj-include 'partial.html' shadow />"
    tag = create_tag(html)

    actual = map_include(tag=tag)

    assert actual == expected
