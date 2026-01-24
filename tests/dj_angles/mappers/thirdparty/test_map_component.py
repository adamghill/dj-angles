import pytest

from dj_angles.exceptions import MissingAttributeError
from dj_angles.mappers.thirdparty import map_component
from tests.dj_angles.tags import create_tag


def test_typical():
    """Basic component with name attribute."""
    expected = "{% component 'calendar' %}"

    html = "<dj-component name='calendar'>"
    tag = create_tag(html)

    actual = map_component(tag=tag)

    assert actual == expected


def test_is_closing():
    """Closing tag."""
    expected = "{% endcomponent %}"

    html = "</dj-component>"
    tag = create_tag(html)

    actual = map_component(tag=tag)

    assert actual == expected


def test_self_closing():
    """Self-closing component."""
    expected = "{% component 'calendar' / %}"

    html = "<dj-component name='calendar' />"
    tag = create_tag(html)

    actual = map_component(tag=tag)

    assert actual == expected


def test_with_attributes():
    """Component with additional attributes."""
    expected = "{% component 'calendar' date='2025-01-22' class='my-calendar' %}"

    html = "<dj-component name='calendar' date='2025-01-22' class='my-calendar'>"
    tag = create_tag(html)

    actual = map_component(tag=tag)

    assert actual == expected


def test_missing_name_attribute():
    """Should raise error when name attribute is missing."""
    html = "<dj-component class='test'>"
    tag = create_tag(html)

    with pytest.raises(MissingAttributeError):
        map_component(tag=tag)


def test_get_django_template_tag(settings):
    """Integration test with default mapper."""
    settings.ANGLES["default_mapper"] = "dj_angles.mappers.thirdparty.map_component"

    expected = "{% component 'calendar' %}"

    html = "<dj-component name='calendar'>"
    tag = create_tag(html)

    actual = tag.get_django_template_tag()

    assert actual == expected


def test_get_django_template_tag_self_closing(settings):
    """Integration test with self-closing tag."""
    settings.ANGLES["default_mapper"] = "dj_angles.mappers.thirdparty.map_component"

    expected = "{% component 'calendar' / %}"

    html = "<dj-component name='calendar' />"
    tag = create_tag(html)

    actual = tag.get_django_template_tag()

    assert actual == expected


def test_get_django_template_tag_is_end(settings):
    """Integration test with end tag."""
    settings.ANGLES["default_mapper"] = "dj_angles.mappers.thirdparty.map_component"

    expected = "{% endcomponent %}"

    html = "</dj-component>"
    tag = create_tag(html)

    actual = tag.get_django_template_tag()

    assert actual == expected


def test_get_django_template_tag_with_attributes(settings):
    """Integration test with attributes."""
    settings.ANGLES["default_mapper"] = "dj_angles.mappers.thirdparty.map_component"

    expected = "{% component 'calendar' date='2025-01-22' %}"

    html = "<dj-component name='calendar' date='2025-01-22'>"
    tag = create_tag(html)

    actual = tag.get_django_template_tag()

    assert actual == expected
