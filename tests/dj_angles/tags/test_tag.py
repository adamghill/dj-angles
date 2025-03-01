from tests.dj_angles.tags import create_tag


def test_get_wrapping_tag_name():
    expected = "dj-include"

    tag = create_tag("<dj-include 'partial.html' />")
    actual = tag.get_wrapping_tag_name()

    assert expected == actual


def test_get_wrapping_tag_name_with_name():
    expected = "dj-hello"

    tag = create_tag("<dj-include 'partial.html' />")
    actual = tag.get_wrapping_tag_name(name="hello")

    assert expected == actual


def test_get_wrapping_tag_name_component():
    expected = "dj-partial"

    tag = create_tag("<dj-partial />")
    actual = tag.get_wrapping_tag_name()

    assert expected == actual


def test_get_wrapping_tag_name_component_with_key():
    expected = "dj-partial-1"

    tag = create_tag("<dj-partial:1 />")
    actual = tag.get_wrapping_tag_name()

    assert expected == actual


def test_default_mapping(settings):
    expected = "<dj-partial>{% include 'partial.html' %}</dj-partial>"

    html = "<dj-partial />"

    tag = create_tag(html)
    actual = tag.get_django_template_tag()

    assert expected == actual


def test_get_attribute_value_or_first_key():
    expected = "'test1'"

    html = "<dj-include template='test1'>"

    tag = create_tag(html)
    actual = tag.get_attribute_value_or_first_key("template")

    assert expected == actual
