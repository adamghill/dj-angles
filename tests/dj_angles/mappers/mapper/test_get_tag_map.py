from dj_angles.mappers.mapper import get_tag_map


def test_default():
    expected = "default_mapper"
    actual = get_tag_map()

    assert len(actual) == 21
    assert actual[None].__name__ == expected


def test_none_default_mapper(settings):
    settings.ANGLES["default_mapper"] = None

    actual = get_tag_map()

    assert len(actual) == 20
    assert actual.get(None) is None
