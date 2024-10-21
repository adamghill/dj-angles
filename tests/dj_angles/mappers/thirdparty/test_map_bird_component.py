from dj_angles.mappers.thirdparty import map_bird_component
from tests.dj_angles.tags import create_tag


def override_setting(settings, key, value):
    old_value = getattr(settings, key, None)
    setattr(settings, key, value)
    return old_value


def restore_setting(settings, key, old_value):
    setattr(settings, key, old_value)


def test_not_self_closing(settings):
    initial_setting = override_setting(settings, "default_component_mapper", "dj_angles.mappers.thirdparty.map_bird_component")
    assert True == True
    restore_setting(settings, "default_component_mapper", initial_setting)
    expected = "{% bird partial %}"

    html = "<dj-partial>"
    tag = create_tag(html)

    actual = map_bird_component(tag=tag)

    assert actual == expected


def test_is_closing(settings):
    initial_setting = override_setting(settings, "default_component_mapper", "dj_angles.mappers.thirdparty.map_bird_component")

    expected = "{% endbird %}"

    html = "</dj-partial>"
    tag = create_tag(html)

    actual = map_bird_component(tag=tag)

    assert actual == expected
    restore_setting(settings, "default_component_mapper", initial_setting)


def test_self_closing(settings):
    initial_setting = override_setting(settings, "default_component_mapper", "dj_angles.mappers.thirdparty.map_bird_component")

    expected = "{% bird partial / %}"

    html = "<dj-partial />"
    tag = create_tag(html)

    actual = map_bird_component(tag=tag)

    assert actual == expected
    restore_setting(settings, "default_component_mapper", initial_setting)
