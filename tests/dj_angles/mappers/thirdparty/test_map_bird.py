from dj_angles.mappers.thirdparty import map_bird
from tests.dj_angles.tags import create_tag


def test_typical():
    expected = "{% bird 'bird-partial' %}"

    html = "<dj-bird 'bird-partial'>"
    tag = create_tag(html)

    actual = map_bird(tag=tag)

    assert actual == expected


def test_typical_tag_name():
    expected = "{% bird bird-partial %}"

    html = "<dj-bird-partial>"
    tag = create_tag(html)

    actual = map_bird(tag=tag)

    assert actual == expected


def test_is_closing():
    expected = "{% endbird %}"

    html = "</dj-bird>"
    tag = create_tag(html)

    actual = map_bird(tag=tag)

    assert actual == expected


def test_is_closing_tag_name():
    expected = "{% endbird %}"

    html = "</dj-bird-partial>"
    tag = create_tag(html)

    actual = map_bird(tag=tag)

    assert actual == expected


def test_self_closing():
    expected = "{% bird 'bird-partial' / %}"

    html = "<dj-bird 'bird-partial' />"
    tag = create_tag(html)

    actual = map_bird(tag=tag)

    assert actual == expected


def test_self_closing_tag_name():
    expected = "{% bird bird-partial / %}"

    html = "<dj-bird-partial />"
    tag = create_tag(html)

    actual = map_bird(tag=tag)

    assert actual == expected


def test_template_attribute():
    expected = "{% bird 'bird-partial' / %}"

    html = "<dj-bird template='bird-partial' />"
    tag = create_tag(html)

    actual = map_bird(tag=tag)

    assert actual == expected


def test_additional_attribute():
    expected = "{% bird 'bird-partial' blob='test' %}"

    html = "<dj-bird template='bird-partial' blob='test'>"
    tag = create_tag(html)

    actual = map_bird(tag=tag)

    assert actual == expected


def test_get_django_template_tag(settings):
    settings.ANGLES["default_mapper"] = "dj_angles.mappers.map_bird"

    expected = "{% bird bird-partial %}"

    html = "<dj-bird-partial>"
    tag = create_tag(html)

    actual = tag.get_django_template_tag()

    assert actual == expected


def test_get_django_template_tag_self_closing(settings):
    settings.ANGLES["default_mapper"] = "dj_angles.mappers.map_bird"

    expected = "{% bird bird-partial / %}"

    html = "<dj-bird-partial />"

    tag = create_tag(html)
    actual = tag.get_django_template_tag()

    assert expected == actual


def test_get_django_template_tag_is_end(settings):
    settings.ANGLES["default_mapper"] = "dj_angles.mappers.map_bird"

    expected = "{% endbird %}"

    html = "</dj-bird-partial>"

    tag = create_tag(html)
    actual = tag.get_django_template_tag()

    assert expected == actual


def test_get_django_template_tag_with_attributes(settings):
    settings.ANGLES["default_mapper"] = "dj_angles.mappers.map_bird"

    expected = "{% bird bird-partial blob='test' %}"

    html = "<dj-bird-partial blob='test'>"

    tag = create_tag(html)
    actual = tag.get_django_template_tag()

    assert expected == actual
