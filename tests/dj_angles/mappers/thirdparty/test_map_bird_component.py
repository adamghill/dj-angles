from dj_angles.mappers.thirdparty import map_bird_component
from tests.dj_angles.tags import create_tag


def test_not_self_closing():
    expected = "{% bird partial %}"

    html = "<dj-partial>"
    tag = create_tag(html)

    actual = map_bird_component(tag=tag)

    assert actual == expected


def test_is_closing():
    expected = "{% endbird %}"

    html = "</dj-partial>"
    tag = create_tag(html)

    actual = map_bird_component(tag=tag)

    assert actual == expected


def test_self_closing():
    expected = "{% bird partial / %}"

    html = "<dj-partial />"
    tag = create_tag(html)

    actual = map_bird_component(tag=tag)

    assert actual == expected


def test_not_self_closing_from_settings(settings):
    settings.ANGLES["default_component_mapper"] = "dj_angles.mappers.thirdparty.map_bird_component"

    expected = "{% bird partial %}"

    html = "<dj-partial>"
    tag = create_tag(html)

    actual = tag.get_django_template_tag()

    assert actual == expected


def test_self_closing_from_settings(settings):
    settings.ANGLES["default_component_mapper"] = "dj_angles.mappers.thirdparty.map_bird_component"

    expected = "{% bird partial / %}"

    html = "<dj-partial />"

    tag = create_tag(html)
    actual = tag.get_django_template_tag()

    assert expected == actual


def test_closing_from_settings(settings):
    settings.ANGLES["default_component_mapper"] = "dj_angles.mappers.thirdparty.map_bird_component"

    expected = "{% endbird %}"

    html = "</dj-partial>"

    tag = create_tag(html)
    actual = tag.get_django_template_tag()

    assert expected == actual
