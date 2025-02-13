from dj_angles.regex_replacer import (
    end_of_tag_index,
    get_end_of_attribute_value,
    get_previous_element_tag,
)


def test_get_end_of_attribute_value():
    assert get_end_of_attribute_value('"hello"', 0) == ("hello", 7)
    assert get_end_of_attribute_value('dj-if="hello"', 6) == ("hello", 13)
    assert get_end_of_attribute_value("dj-if='hello'", 6) == ("hello", 13)
    assert get_end_of_attribute_value("dj-if=hello", 6) == ("hello", 11)
    assert get_end_of_attribute_value("dj-if=hello there", 6) == ("hello", 11)
    assert get_end_of_attribute_value("dj-if=hello.there", 6) == ("hello.there", 17)
    assert get_end_of_attribute_value("dj-if=hello><span></span>", 6) == ("hello", 11)


def test_get_previous_element_tag():
    assert get_previous_element_tag("<div dj-if='hello'>test</div>", 4) == ("div", 0)
    assert get_previous_element_tag("<span dj-if=hello>test</div>", 5) == ("span", 0)
    assert get_previous_element_tag("<p dj-if=hello there>test</div>", 2) == ("p", 0)
    assert get_previous_element_tag("<div dj-if=hello.there>test</div>", 4) == ("div", 0)
    assert get_previous_element_tag("<div><div dj-if=hello.there>test</div></div>", 10) == ("div", 5)


def test_end_of_tag_index():
    assert end_of_tag_index("<div dj-if='hello'>test</div>", 4, "div") == 29
    assert end_of_tag_index("<div dj-if='hello'><div>test</div></div>", 4, "div") == 40
    assert end_of_tag_index("<div dj-if='hello'><div>test</div></div>", 20, "div") == 34
    assert end_of_tag_index("<div dj-if='hello'><span>test</span></div>", 20, "div") == 42

    expected = 61
    html = """
<div dj-if='hello'>
    <div>
        test
    </div>
</div><div><p>hello</p></div>"""
    actual = end_of_tag_index(html, 4, "div")
    assert actual == expected

    assert end_of_tag_index("<img dj-if='hello' />", 4, "img") == 21
    assert end_of_tag_index("<img dj-if='hello'>", 4, "img") == 19
