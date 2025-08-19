import pytest
from tests.dj_angles.tags import create_tag

from dj_angles.exceptions import InvalidAttributeError
from dj_angles.mappers.include import map_include


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


def test_template_attribute():
    expected = "<dj-partial>{% include 'partial.html' %}</dj-partial>"

    html = "<dj-include template='partial.html' />"
    tag = create_tag(html)

    actual = map_include(tag=tag)

    assert actual == expected


def test_class():
    expected = "<dj-partial class='mt-2 mb-4'>{% include 'partial.html' %}</dj-partial>"

    html = "<dj-include template='partial.html' class='mt-2 mb-4' />"
    tag = create_tag(html)

    actual = map_include(tag=tag)

    assert actual == expected


def test_no_wrap():
    expected = "{% include 'partial.html' %}"

    html = "<dj-include template='partial.html' no-wrap />"
    tag = create_tag(html)

    actual = map_include(tag=tag)

    assert actual == expected


def test_no_wrap_and_class():
    html = "<dj-include template='partial.html' no-wrap class='mt-2' />"
    tag = create_tag(html)

    with pytest.raises(InvalidAttributeError) as e:
        map_include(tag=tag)

    assert (
        e.exconly()
        == "dj_angles.exceptions.InvalidAttributeError: `no-wrap` and `class` attributes cannot be used together"
    )


def test_no_wrap_and_empty_class():
    html = "<dj-include template='partial.html' no-wrap class='' />"
    expected = "{% include 'partial.html' %}"

    tag = create_tag(html)

    actual = map_include(tag=tag)

    assert actual == expected
