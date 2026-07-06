import re

from dj_angles.replacers.attributes.elements import Element


def test_find_element_basic():
    html = '<div dj-value="x">content</div>'
    match = re.search(r"dj-value=\"x\"", html)

    element = Element.from_match(html, match, "value")

    assert element.tag_name == "div"
    assert element.tag_start == 0
    assert element.tag_end == 18
    assert element.full_end == 31
    assert element.original_tag == '<div dj-value="x">'
    assert element.original_full == '<div dj-value="x">content</div>'
    assert element.is_closing is False


def test_find_element_self_closing():
    html = '<img dj-value="x" />'
    match = re.search(r"dj-value=\"x\"", html)

    element = Element.from_match(html, match, "value")

    assert element.tag_name == "img"
    assert element.original_tag == '<img dj-value="x" />'
    assert element.full_end == element.tag_end
    assert element.is_closing is False


def test_find_element_void():
    html = '<input dj-value="x">'
    match = re.search(r"dj-value=\"x\"", html)

    element = Element.from_match(html, match, "value")

    assert element.tag_name == "input"
    assert element.original_tag == '<input dj-value="x">'
    assert element.full_end == element.tag_end


def test_find_element_closing_tag():
    html = '</div dj-value="x">'
    match = re.search(r"dj-value=\"x\"", html)

    element = Element.from_match(html, match, "value")

    assert element.tag_name == "div"
    assert element.is_closing is True


def test_find_element_nested():
    html = '<div dj-value="outer"><span dj-value="inner"></span></div>'
    matches = list(re.finditer(r"dj-value=\"[^\"]+\"", html))

    outer = Element.from_match(html, matches[0], "value")
    inner = Element.from_match(html, matches[1], "value")

    assert outer.contains(inner) is True
    assert inner.contains(outer) is False


def test_element_remove_attribute():
    html = '<div class="foo" dj-value="x">content</div>'
    match = re.search(r"dj-value=\"x\"", html)

    element = Element.from_match(html, match, "value")

    assert element.remove_attribute() == '<div class="foo">'


def test_element_closing_tag():
    html = '<div dj-value="x">content</div>'
    match = re.search(r"dj-value=\"x\"", html)

    element = Element.from_match(html, match, "value")

    assert element.closing_tag() == "</div>"


def test_element_closing_tag_generated():
    html = '<img dj-value="x" />'
    match = re.search(r"dj-value=\"x\"", html)

    element = Element.from_match(html, match, "value")

    assert element.closing_tag() == "</img>"


def test_element_type_and_value_fields():
    html = '<div dj-value="x">content</div>'
    match = re.search(r"dj-value=\"x\"", html)

    element = Element.from_match(html, match, "value")
    element.value = "x"

    assert element.type == "value"
    assert element.value == "x"
