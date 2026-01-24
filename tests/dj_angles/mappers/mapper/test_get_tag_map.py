from unittest.mock import patch

from dj_angles.mappers.mapper import TagMap, get_tag_map


def test_default():
    expected = "default_mapper"
    actual = get_tag_map()

    assert len(actual) == 27

    # Check for optional mappers
    assert "partial" in actual.keys()
    assert "bird" in actual.keys()
    assert "component" in actual.keys()

    # Check for default mapper
    assert actual[None].__name__ == expected


def test_none_default_mapper(settings):
    settings.ANGLES["default_mapper"] = None

    actual = get_tag_map()

    assert len(actual) == 26

    # Check for optional mappers
    assert "partial" in actual.keys()
    assert "bird" in actual.keys()
    assert "component" in actual.keys()

    # Check that there is no default mapper
    assert actual.get(None) is None


def test_django_6_version_enables_partial():
    with patch("dj_angles.mappers.mapper.django.VERSION", (6, 0, 0)):
        with patch("dj_angles.mappers.mapper.is_module_available", return_value=False):
            tag_map = TagMap()
            assert "partial" in tag_map


def test_django_old_version_disables_partial():
    with patch("dj_angles.mappers.mapper.django.VERSION", (4, 2, 0)):
        with patch("dj_angles.mappers.mapper.is_module_available", return_value=False):
            tag_map = TagMap()
            assert "partial" not in tag_map
