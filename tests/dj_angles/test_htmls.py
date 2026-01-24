import pytest

from dj_angles.htmls import find_character, get_outer_html


def test_get_outer_html_simple():
    html = "<div>content</div>"
    tag = get_outer_html(html, 0)

    assert tag is not None
    assert tag.outer_html == "<div>content</div>"
    assert tag.tag_name == "div"


def test_get_outer_html_with_attributes():
    html = "<div class='foo' id=\"bar\">content</div>"
    tag = get_outer_html(html, 0)

    assert tag is not None
    assert tag.outer_html == "<div class='foo' id=\"bar\">content</div>"


def test_get_outer_html_nested():
    html = "<div><span>nested</span></div>"
    tag = get_outer_html(html, 0)

    assert tag is not None
    assert tag.outer_html == "<div><span>nested</span></div>"


def test_get_outer_html_from_offset():
    html = "<span>prev</span><div>target</div>"
    tag = get_outer_html(html, 13)

    assert tag is not None
    assert tag.outer_html == "<div>target</div>"
    assert tag.tag_name == "div"


def test_get_outer_html_self_closing():
    html = "<img src='foo.jpg' />"
    tag = get_outer_html(html, 0)

    assert tag is not None
    assert tag.outer_html == "<img src='foo.jpg' />"
    assert tag.is_self_closing


def test_get_outer_html_void_element():
    # Void elements like <input> don't technically need /> but Tag might handle them specifically
    html = "<input type='text'>"
    tag = get_outer_html(html, 0)

    assert tag is not None
    assert tag.outer_html == "<input type='text'>"


def test_get_outer_html_not_found():
    html = "text only"
    tag = get_outer_html(html, 0)

    assert tag is None


def test_get_outer_html_incomplete():
    html = "<div>incomplete"
    tag = get_outer_html(html, 0)

    assert tag is None


def test_get_outer_html_nested_same_tag():
    html = "<div><div>inner</div></div>"
    tag = get_outer_html(html, 0)

    assert tag is not None
    assert tag.outer_html == "<div><div>inner</div></div>"


def test_get_outer_html_nested_self_closing():
    html = "<div><div /></div>"
    tag = get_outer_html(html, 0)

    assert tag is not None
    assert tag.outer_html == "<div><div /></div>"


def test_get_outer_html_with_quotes():
    html = "<div data-val='>'>content</div>"
    tag = get_outer_html(html, 0)

    assert tag is not None
    assert tag.outer_html == "<div data-val='>'>content</div>"


def test_find_character_basic():
    html = "012345"
    assert find_character(html, 0, character="3") == 3
    assert find_character(html, 0, character="9") == -1


def test_find_character_regex():
    html = "012345"
    assert find_character(html, 0, character_regex=r"[3-4]") == 3


def test_find_character_reverse():
    html = "012345"
    assert find_character(html, 5, character="2", reverse=True) == 2


def test_find_character_with_quotes():
    html = "0'23'5"
    assert find_character(html, 0, character="2") == -1

    html2 = '0"23"5'
    assert find_character(html2, 0, character="2") == -1


def test_find_character_errors():
    with pytest.raises(ValueError):
        find_character("abc", 0)
