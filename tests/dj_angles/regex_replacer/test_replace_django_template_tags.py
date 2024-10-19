import pytest

from dj_angles.exceptions import InvalidEndTagError
from dj_angles.regex_replacer import replace_django_template_tags


def test_typical():
    expected = """{% extends 'base.html' %}

{% block content %}
  <input />

  <dj-partial>{% include 'partial.html' %}</dj-partial>

  <dj-partial>{% include 'partial.html' %}</dj-partial>

  <dj-partial>{% include 'partial.html' %}</dj-partial>

  <dj-another-directory-another-partial>{% include 'another-directory/another-partial.html' %}</dj-another-directory-another-partial>

  {% debug %}
{% endblock content %}"""  # noqa: E501

    template = """<dj-extends 'base.html' />

<dj-block content>
  <input />

  <dj-partial />

  <dj-include 'partial'></dj-include 'partial'>

  <dj-include 'partial'></dj-include>

  <dj-another-directory/another-partial />

  <dj-debug />
</dj-block content>"""
    actual = replace_django_template_tags(template)

    assert actual == expected


def test_short_include():
    expected = "<dj-partial>{% include 'partial.html' %}</dj-partial>"

    template = "<dj-partial></dj-partial>"
    actual = replace_django_template_tags(template)

    assert actual == expected


def test_short_include_self_closing():
    expected = "<dj-partial>{% include 'partial.html' %}</dj-partial>"

    template = "<dj-partial />"
    actual = replace_django_template_tags(template)

    assert actual == expected


def test_short_include_shadow_no_end_tag_shadow():
    expected = "<dj-partial><template shadowrootmode='open'>{% include 'partial.html' %}</template></dj-partial>"

    template = "<dj-partial!></dj-partial>"
    actual = replace_django_template_tags(template)

    assert actual == expected


def test_short_include_shadow():
    expected = "<dj-partial><template shadowrootmode='open'>{% include 'partial.html' %}</template></dj-partial>"

    template = "<dj-partial!></dj-partial!>"
    actual = replace_django_template_tags(template)

    assert actual == expected


def test_short_include_self_closing_shadow():
    expected = "<dj-partial><template shadowrootmode='open'>{% include 'partial.html' %}</template></dj-partial>"

    template = "<dj-partial! />"
    actual = replace_django_template_tags(template)

    assert actual == expected


def test_include_no_extension():
    expected = "<dj-partial>{% include 'partial.html' %}</dj-partial>"

    template = "<dj-include 'partial'></dj-include>"
    actual = replace_django_template_tags(template)

    assert actual == expected


def test_include_no_extension_self_closing():
    expected = "<dj-partial>{% include 'partial.html' %}</dj-partial>"

    template = "<dj-include 'partial' />"
    actual = replace_django_template_tags(template)

    assert actual == expected


def test_include_extension():
    expected = "<dj-partial>{% include 'partial.html' %}</dj-partial>"

    template = "<dj-include 'partial.html'></dj-include>"
    actual = replace_django_template_tags(template)

    assert actual == expected


def test_include_extension_self_closing():
    expected = "<dj-partial>{% include 'partial.html' %}</dj-partial>"

    template = "<dj-include 'partial.html' />"
    actual = replace_django_template_tags(template)

    assert actual == expected


def test_include_template_no_extension():
    expected = "<dj-partial>{% include 'partial.html' %}</dj-partial>"

    template = "<dj-include template='partial'></dj-include>"
    actual = replace_django_template_tags(template)

    assert actual == expected


def test_include_template_no_extension_self_closing():
    expected = "<dj-partial>{% include 'partial.html' %}</dj-partial>"

    template = "<dj-include template='partial' />"
    actual = replace_django_template_tags(template)

    assert actual == expected


def test_include_template_extension():
    expected = "<dj-partial>{% include 'partial.html' %}</dj-partial>"

    template = "<dj-include template='partial.html'></dj-include>"
    actual = replace_django_template_tags(template)

    assert actual == expected


def test_include_template_extension_self_closing():
    expected = "<dj-partial>{% include 'partial.html' %}</dj-partial>"

    template = "<dj-include template='partial.html' />"
    actual = replace_django_template_tags(template)

    assert actual == expected


def test_invalid_tag():
    with pytest.raises(InvalidEndTagError) as e:
        replace_django_template_tags("""
<dj-block content>
<input>

<dj-partial>
</dj-block content>""")

    assert e.exconly() == "dj_angles.exceptions.InvalidEndTagError"
    assert e.value.tag.component_name == "block"
    assert e.value.last_tag.component_name == "partial"


def test_extends():
    expected = "{% extends 'base.html' %}"
    actual = replace_django_template_tags("<dj-extends 'base.html' />")

    assert actual == expected
