from dj_angles.mappers.django import map_autoescape
from tests.dj_angles.tags import create_tag


def test_map_autoescape_on():
    html = "<dj-autoescape on>"
    tag = create_tag(html)
    assert map_autoescape(tag) == "{% autoescape on %}"


def test_map_autoescape_off():
    html = "<dj-autoescape off>"
    tag = create_tag(html)
    assert map_autoescape(tag) == "{% autoescape off %}"


def test_map_endautoescape():
    html = "</dj-autoescape>"
    tag = create_tag(html)
    assert map_autoescape(tag) == "{% endautoescape %}"
