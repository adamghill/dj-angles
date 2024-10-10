import pytest

from dj_angles.exceptions import MissingAttributeError
from dj_angles.mappers import map_extends
from tests.dj_angles.tags import create_tag


def test_string():
    expected = "{% extends 'base.html' %}"

    html = "<dj-extends 'base.html'>"
    tag = create_tag(html)

    actual = map_extends(tag=tag)

    assert actual == expected


def test_parent_attribute():
    expected = "{% extends 'base.html' %}"

    html = "<dj-extends parent='base.html'>"
    tag = create_tag(html)

    actual = map_extends(tag=tag)

    assert actual == expected


def test_missing_parent_throws_exception():
    html = "<dj-extends invalid='base.html'>"
    tag = create_tag(html)

    with pytest.raises(MissingAttributeError) as e:
        map_extends(tag=tag)

    assert e.value.name == "parent"
