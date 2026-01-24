import pytest

from dj_angles.exceptions import InvalidEndTagError, MissingAttributeError
from dj_angles.mappers.django import map_block
from tests.dj_angles.tags import create_tag


def test_string():
    expected = "{% block content %}"

    html = "<dj-block 'content'>"
    tag = create_tag(html)

    actual = map_block(tag=tag)

    assert actual == expected


def test_is_end():
    expected = "{% endblock %}"

    html = "</dj-block>"
    tag = create_tag(html)

    actual = map_block(tag=tag)

    assert actual == expected


def test_name_attribute():
    expected = "{% block content %}"

    html = "<dj-block name='content'>"
    tag = create_tag(html)

    actual = map_block(tag=tag)

    assert actual == expected


def test_name_self_closing():
    expected = "{% block content %}{% endblock content %}"

    html = "<dj-block 'content' />"
    tag = create_tag(html)

    actual = map_block(tag=tag)

    assert actual == expected


def test_name_attribute_self_closing():
    expected = "{% block content %}{% endblock content %}"

    html = "<dj-block name='content' />"
    tag = create_tag(html)

    actual = map_block(tag=tag)

    assert actual == expected


def test_missing_name_throws_exception():
    html = "<dj-block invalid='content'>"
    tag = create_tag(html)

    with pytest.raises(MissingAttributeError) as e:
        map_block(tag=tag)

    assert e.value.name == "name"


def test_missing_attributes_throws_exception():
    html = "<dj-block>"
    tag = create_tag(html)

    with pytest.raises(Exception) as e:
        map_block(tag=tag)

    assert str(e.value) == "Missing name"


def test_endblock_mismatch_throws_exception():
    # We need to construct a tag that has a start_tag with a different name

    html_start = "<dj-block name='start'>"
    start_tag = create_tag(html_start)
    start_tag.parse_attributes()

    html_end = "</dj-block name='end'>"
    end_tag = create_tag(html_end)
    end_tag.start_tag = start_tag

    with pytest.raises(InvalidEndTagError):
        map_block(tag=end_tag)


def test_endblock_with_name_matching_start():
    html_start = "<dj-block name='content'>"
    start_tag = create_tag(html_start)
    start_tag.parse_attributes()

    html_end = "</dj-block name='content'>"
    end_tag = create_tag(html_end)
    end_tag.start_tag = start_tag

    expected = "{% endblock content %}"
    actual = map_block(tag=end_tag)
    assert actual == expected
