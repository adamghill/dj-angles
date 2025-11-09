from dj_angles.mappers.thirdparty import map_partialdef
from tests.dj_angles.tags import create_tag


def test_typical():
    expected = "{% partialdef test1 %}"

    html = "<dj-partial name='test1'>"
    tag = create_tag(html)

    actual = map_partialdef(tag=tag)

    assert actual == expected


def test_typical_no_name():
    expected = "{% partialdef test1 %}"

    html = "<dj-partial 'test1'>"
    tag = create_tag(html)

    actual = map_partialdef(tag=tag)

    assert actual == expected


def test_is_closing():
    expected = "{% endpartialdef %}"

    html = "</dj-partial>"
    tag = create_tag(html)

    actual = map_partialdef(tag=tag)

    assert actual == expected


def test_get_django_template_tag(settings):
    settings.ANGLES["default_mapper"] = "dj_angles.mappers.map_partialdef"

    expected = "{% partialdef test1 %}"

    html = "<dj-partial name='test1'>"
    tag = create_tag(html)

    actual = tag.get_django_template_tag()

    assert actual == expected


def test_get_django_template_tag_is_end(settings):
    settings.ANGLES["default_mapper"] = "dj_angles.mappers.map_partialdef"

    expected = "{% endpartialdef %}"

    html = "</dj-partial>"

    tag = create_tag(html)
    actual = tag.get_django_template_tag()

    assert expected == actual
