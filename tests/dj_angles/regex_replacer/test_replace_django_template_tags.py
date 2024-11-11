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


def test_block():
    expected = """
{% block content %}
{% endblock content %}"""

    template = """
<dj-block name="content">
</dj-block name="content">"""
    actual = replace_django_template_tags(template)

    assert actual == expected


def test_block_default():
    expected = "{% block content %}default{% endblock content %}"

    template = '<dj-block name="content">default</dj-block>'
    actual = replace_django_template_tags(template)

    assert actual == expected


def test_block_different_name():
    template = """
<dj-block name="content1">
</dj-block  name="content2">"""

    with pytest.raises(InvalidEndTagError):
        replace_django_template_tags(template)


def test_block_missing_end_name():
    expected = """
{% block content %}
{% endblock content %}"""

    template = """
<dj-block name="content">
</dj-block>"""
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
    assert e.value.tag.tag_name == "block"
    assert e.value.last_tag.tag_name == "partial"


def test_extends():
    expected = "{% extends 'base.html' %}"
    actual = replace_django_template_tags("<dj-extends 'base.html' />")

    assert actual == expected


def test_slot(settings):
    settings.ANGLES["slots_enabled"] = True

    expected = """
<dj-slot><div>
<slot name="test1"><span slot="test1">new slot1</span></slot>
<slot name="test2">slot2</slot>
</div>

</dj-slot>

<dj-slot><div>
<slot name="test1">slot1</slot>
<slot name="test2"><span slot="test2">new slot2</span></slot>
</div>

</dj-slot>
"""

    template = """
<dj-include template='slot.html'>
<span slot="test1">new slot1</span>
</dj-include>

<dj-include template='slot.html'>
<span slot="test2">new slot2</span>
</dj-include>
"""
    actual = replace_django_template_tags(template)

    assert actual == expected


def test_slot_missing_template(settings):
    settings.ANGLES["slots_enabled"] = True

    expected = """
<dj-test_slot_missing_template>

</dj-test_slot_missing_template>

<dj-test_slot_missing_template>

</dj-test_slot_missing_template>
"""

    template = """
<dj-include template='test_slot_missing_template.html'>
<span slot="test1">This is the new slot.</span>
</dj-include>

<dj-include template='test_slot_missing_template.html'>
<span slot="test2">This is the new slot.</span>
</dj-include>
"""
    actual = replace_django_template_tags(template)

    assert actual == expected


def test_short_include_underscore():
    """Makes sure that if a real template with the file name '_underscore.html' is available,
    that is the template file that should be used.
    """

    expected = "<dj-underscore>{% include '_underscore.html' %}</dj-underscore>"

    template = "<dj-underscore></dj-underscore>"
    actual = replace_django_template_tags(template)

    assert actual == expected


def test_short_include_underscore_in_subdirectory():
    """Makes sure that if a real template with the file name 'components/_underscore.html' is available,
    that is the template file that should be used.
    """

    expected = "<dj-components-underscore>{% include 'components/_underscore.html' %}</dj-components-underscore>"

    template = "<dj-components/underscore></dj-components/underscore>"
    actual = replace_django_template_tags(template)

    assert actual == expected
