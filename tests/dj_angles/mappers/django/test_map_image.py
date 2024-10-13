import pytest

from dj_angles.exceptions import MissingAttributeError
from dj_angles.mappers.django import map_image
from tests.dj_angles.tags import create_tag


def test_string():
    expected = "<img src=\"{% static 'img/blob.png' %}\" />"

    html = "<dj-image 'img/blob.png' />"
    tag = create_tag(html)

    actual = map_image(tag=tag)

    assert actual == expected


def test_src_attribute():
    expected = "<img src=\"{% static 'img/blob.png' %}\" />"

    html = "<dj-image src='img/blob.png' />"
    tag = create_tag(html)

    actual = map_image(tag=tag)

    assert actual == expected


def test_src_second_attribute():
    expected = "<img src=\"{% static 'img/blob.png' %}\" width='100' />"

    html = "<dj-image width='100' src='img/blob.png' />"
    tag = create_tag(html)

    actual = map_image(tag=tag)

    assert actual == expected


def test_missing_src_throws_exception():
    html = "<dj-image invalid='img/blob.png' />"
    tag = create_tag(html)

    with pytest.raises(MissingAttributeError) as e:
        map_image(tag=tag)

    assert e.value.name == "src"
