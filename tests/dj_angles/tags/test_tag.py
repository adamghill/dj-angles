import pytest

from dj_angles.exceptions import MissingAttributeError
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
    expected = "dj-fake-partial"

    tag = create_tag("<dj-fake-partial />")
    actual = tag.get_wrapping_tag_name()

    assert expected == actual


def test_get_wrapping_tag_name_component_with_key():
    expected = "dj-partial-1"

    tag = create_tag("<dj-partial:1 />")
    actual = tag.get_wrapping_tag_name()

    assert expected == actual


def test_default_mapping(settings):
    expected = "<dj-fake-partial>{% include 'fake-partial.html' %}</dj-fake-partial>"

    html = "<dj-fake-partial />"

    tag = create_tag(html)
    actual = tag.get_django_template_tag()

    assert expected == actual


def test_pop_attribute_value_or_first_key():
    expected = "'test1'"

    html = "<dj-include template='test1'>"

    tag = create_tag(html)
    actual = tag.pop_attribute_value_or_first_key("template")

    assert expected == actual


def test_tag_repr():
    tag = create_tag(html="<dj-div>")
    assert str(tag) == "<dj-div>"


def test_wrapping_tag_name_with_bang():
    tag = create_tag(html="<dj-div>")
    wrapping = tag.get_wrapping_tag_name(name="foo!")
    assert wrapping == "dj-foo"


def test_component_name_property():
    tag = create_tag(html="<dj-test>")
    assert tag.component_name == "test"


def test_is_wrapped_attribute():
    tag = create_tag(html="<dj-test no-wrap>")
    assert tag.is_wrapped is False


def test_shadow_attribute():
    tag = create_tag(html="<dj-test shadow>")
    assert tag.is_shadow is True


def test_shadow_bang():
    tag = create_tag(html="<dj-test!>")
    assert tag.is_shadow is True
    assert tag.tag_name == "test"


def test_missing_attribute_error_from_pop_attribute():
    tag = create_tag(html="<dj-test>")
    with pytest.raises(MissingAttributeError):
        tag.pop_attribute_value_or_first_key("missing")
