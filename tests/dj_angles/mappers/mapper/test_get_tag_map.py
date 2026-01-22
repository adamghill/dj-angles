from unittest.mock import patch

from dj_angles.mappers.mapper import TagMap, get_tag_map


def test_default():
    expected = "default_mapper"
    actual = get_tag_map()

    assert len(actual) == 25
    assert actual[None].__name__ == expected


def test_none_default_mapper(settings):
    settings.ANGLES["default_mapper"] = None

    actual = get_tag_map()

    assert len(actual) == 24
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
