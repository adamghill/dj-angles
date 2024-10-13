import pytest

from dj_angles.exceptions import MissingAttributeError
from dj_angles.mappers.django import map_css
from tests.dj_angles.tags import create_tag


def test_string():
    expected = '<link href="{% static \'css/style.css\' %}" rel="stylesheet" />'

    html = "<dj-css 'css/style.css' />"
    tag = create_tag(html)

    actual = map_css(tag=tag)

    assert actual == expected


def test_href_attribute():
    expected = '<link href="{% static \'css/style.css\' %}" rel="stylesheet" />'

    html = "<dj-css href='css/style.css' />"
    tag = create_tag(html)

    actual = map_css(tag=tag)

    assert actual == expected


def test_href_second_attribute():
    expected = "<link href=\"{% static 'css/style.css' %}\" invalid='css/style1.css' rel=\"stylesheet\" />"

    html = "<dj-css invalid='css/style1.css' href='css/style.css' />"
    tag = create_tag(html)

    actual = map_css(tag=tag)

    assert actual == expected


def test_missing_href_throws_exception():
    html = "<dj-css invalid='css/style1.css' />"
    tag = create_tag(html)

    with pytest.raises(MissingAttributeError) as e:
        map_css(tag=tag)

    assert e.value.name == "href"
