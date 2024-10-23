from tests.dj_angles.tags import create_tag

from dj_angles.mappers.include import get_include_template_file


def test_first_attribute():
    expected = "'partial.html'"

    html = "<dj-include 'partial'>"
    tag = create_tag(html)

    actual = get_include_template_file(tag=tag)

    assert actual == expected


def test_first_attribute_with_extension():
    expected = "'partial.html'"

    html = "<dj-include 'partial.html'>"
    tag = create_tag(html)

    actual = get_include_template_file(tag=tag)

    assert actual == expected


def test_first_attribute_double_quote():
    expected = '"partial.html"'

    html = '<dj-include "partial">'
    tag = create_tag(html)

    actual = get_include_template_file(tag=tag)

    assert actual == expected


def test_template_attribute():
    expected = "'partial.html'"

    html = "<dj-include template='partial'>"
    tag = create_tag(html)

    actual = get_include_template_file(tag=tag)

    assert actual == expected


def test_template_attribute_with_extension():
    expected = "'partial.html'"

    html = "<dj-include template='partial.html'>"
    tag = create_tag(html)

    actual = get_include_template_file(tag=tag)

    assert actual == expected


def test_template_attribute_double_quote():
    expected = '"partial.html"'

    html = '<dj-include template="partial">'
    tag = create_tag(html)

    actual = get_include_template_file(tag=tag)

    assert actual == expected


def test_fallback():
    expected = "'partial.html'"

    html = "<dj-partial>"
    tag = create_tag(html)

    actual = get_include_template_file(tag=tag)

    assert actual == expected
