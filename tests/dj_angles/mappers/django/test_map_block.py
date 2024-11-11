import pytest

from dj_angles.exceptions import MissingAttributeError
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
