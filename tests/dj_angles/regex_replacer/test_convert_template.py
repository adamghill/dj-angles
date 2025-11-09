import pytest

from dj_angles.exceptions import InvalidEndTagError
from dj_angles.regex_replacer import convert_template


def test_typical():
    expected = """{% extends 'base.html' %}

{% block content %}
  <input />

  <dj-fake-partial>{% include 'fake-partial.html' %}</dj-fake-partial>

  <dj-fake-partial>{% include 'fake-partial.html' %}</dj-fake-partial>

  <dj-fake-partial>{% include 'fake-partial.html' %}</dj-fake-partial>

  <dj-another-directory-another-partial>{% include 'another-directory/another-partial.html' %}</dj-another-directory-another-partial>

  {% debug %}
{% endblock content %}"""  # noqa: E501

    template = """<dj-extends 'base.html' />

<dj-block content>
  <input />

  <dj-fake-partial />

  <dj-include 'fake-partial'></dj-include 'fake-partial'>

  <dj-include 'fake-partial'></dj-include>

  <dj-another-directory/another-partial />

  <dj-debug />
</dj-block content>"""
    actual = convert_template(template)

    assert actual == expected


def test_block():
    expected = """
{% block content %}
{% endblock content %}"""

    template = """
<dj-block name="content">
</dj-block name="content">"""
    actual = convert_template(template)

    assert actual == expected


def test_block_default():
    expected = "{% block content %}default{% endblock content %}"

    template = '<dj-block name="content">default</dj-block>'
    actual = convert_template(template)

    assert actual == expected


def test_block_different_name():
    template = """
<dj-block name="content1">
</dj-block  name="content2">"""

    with pytest.raises(InvalidEndTagError):
        convert_template(template)


def test_block_missing_end_name():
    expected = """
{% block content %}
{% endblock content %}"""

    template = """
<dj-block name="content">
</dj-block>"""
    actual = convert_template(template)

    assert actual == expected


def test_short_include():
    expected = "<dj-fake-partial>{% include 'fake-partial.html' %}</dj-fake-partial>"

    template = "<dj-fake-partial></dj-fake-partial>"
    actual = convert_template(template)

    assert actual == expected


def test_short_include_self_closing():
    expected = "<dj-fake-partial>{% include 'fake-partial.html' %}</dj-fake-partial>"

    template = "<dj-fake-partial />"
    actual = convert_template(template)

    assert actual == expected


def test_short_include_shadow_no_end_tag_shadow():
    expected = "<dj-fake-partial><template shadowrootmode='open'>{% include 'fake-partial.html' %}</template></dj-fake-partial>"  # noqa: E501

    template = "<dj-fake-partial!></dj-fake-partial>"
    actual = convert_template(template)

    assert actual == expected


def test_short_include_shadow():
    expected = "<dj-fake-partial><template shadowrootmode='open'>{% include 'fake-partial.html' %}</template></dj-fake-partial>"  # noqa: E501

    template = "<dj-fake-partial!></dj-fake-partial!>"
    actual = convert_template(template)

    assert actual == expected


def test_short_include_self_closing_shadow_bang():
    expected = "<dj-fake-partial><template shadowrootmode='open'>{% include 'fake-partial.html' %}</template></dj-fake-partial>"  # noqa: E501

    template = "<dj-fake-partial! />"
    actual = convert_template(template)

    assert actual == expected


def test_short_include_self_closing_shadow():
    expected = "<dj-partial><template shadowrootmode='open'>{% include 'partial.html' %}</template></dj-partial>"

    template = "<dj-include template='partial.html' shadow />"
    actual = convert_template(template)

    assert actual == expected


def test_include_no_extension():
    expected = "<dj-partial>{% include 'partial.html' %}</dj-partial>"

    template = "<dj-include 'partial'></dj-include>"
    actual = convert_template(template)

    assert actual == expected


def test_include_no_extension_self_closing():
    expected = "<dj-partial>{% include 'partial.html' %}</dj-partial>"

    template = "<dj-include 'partial' />"
    actual = convert_template(template)

    assert actual == expected


def test_include_extension():
    expected = "<dj-partial>{% include 'partial.html' %}</dj-partial>"

    template = "<dj-include 'partial.html'></dj-include>"
    actual = convert_template(template)

    assert actual == expected


def test_include_extension_self_closing():
    expected = "<dj-partial>{% include 'partial.html' %}</dj-partial>"

    template = "<dj-include 'partial.html' />"
    actual = convert_template(template)

    assert actual == expected


def test_include_template_no_extension():
    expected = "<dj-partial>{% include 'partial.html' %}</dj-partial>"

    template = "<dj-include template='partial'></dj-include>"
    actual = convert_template(template)

    assert actual == expected


def test_include_template_no_extension_self_closing():
    expected = "<dj-partial>{% include 'partial.html' %}</dj-partial>"

    template = "<dj-include template='partial' />"
    actual = convert_template(template)

    assert actual == expected


def test_include_template_extension():
    expected = "<dj-partial>{% include 'partial.html' %}</dj-partial>"

    template = "<dj-include template='partial.html'></dj-include>"
    actual = convert_template(template)

    assert actual == expected


def test_include_template_extension_self_closing():
    expected = "<dj-partial>{% include 'partial.html' %}</dj-partial>"

    template = "<dj-include template='partial.html' />"
    actual = convert_template(template)

    assert actual == expected


def test_include_arguments_with_newlines():
    expected = "<dj-fake-partial>{% include 'fake-partial.html' with blob=True stuff=True %}</dj-fake-partial>"

    template = """<dj-fake-partial with blob=True
stuff=True></dj-fake-partial>"""
    actual = convert_template(template)

    assert actual == expected


def test_include_arguments_with_newlines_and_extra_spaces():
    expected = "<dj-fake-partial>{% include 'fake-partial.html' with blob=True stuff=True %}</dj-fake-partial>"

    template = """<dj-fake-partial with blob=True
    stuff=True></dj-fake-partial>"""
    actual = convert_template(template)

    assert actual == expected


def test_include_arguments_with_newlines_and_tab():
    expected = "<dj-fake-partial>{% include 'fake-partial.html' with blob=True stuff=True %}</dj-fake-partial>"

    template = """<dj-fake-partial with blob=True
	stuff=True></dj-fake-partial>"""
    actual = convert_template(template)

    assert actual == expected


def test_invalid_tag():
    with pytest.raises(InvalidEndTagError) as e:
        convert_template("""
<dj-block content>
<input>

<dj-fake-partial>
</dj-block content>""")

    assert e.exconly() == "dj_angles.exceptions.InvalidEndTagError"
    assert e.value.tag.tag_name == "block"
    assert e.value.last_tag.tag_name == "fake-partial"


def test_extends():
    expected = "{% extends 'base.html' %}"
    actual = convert_template("<dj-extends 'base.html' />")

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
    actual = convert_template(template)

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
    actual = convert_template(template)

    assert actual == expected


def test_short_include_underscore():
    """Makes sure that if a real template with the file name '_underscore.html' is available,
    that is the template file that should be used.
    """

    expected = "<dj-underscore>{% include '_underscore.html' %}</dj-underscore>"

    template = "<dj-underscore></dj-underscore>"
    actual = convert_template(template)

    assert actual == expected


def test_short_include_underscore_in_subdirectory():
    """Makes sure that if a real template with the file name 'components/_underscore.html' is available,
    that is the template file that should be used.
    """

    expected = "<dj-components-underscore>{% include 'components/_underscore.html' %}</dj-components-underscore>"

    template = "<dj-components/underscore></dj-components/underscore>"
    actual = convert_template(template)

    assert actual == expected


def test_with():
    expected = '<dj-www-components-include>{% include "www/components/include.html" with request=request only %}\
</dj-www-components-include>'

    template = '<dj-include src="www/components/include.html" with request=request only></dj-include>'
    actual = convert_template(template)

    assert actual == expected


def test_with_only():
    expected = '<dj-www-components-include>{% include "www/components/include.html" with request=request %}\
</dj-www-components-include>'

    template = '<dj-include src="www/components/include.html" with request=request></dj-include>'
    actual = convert_template(template)

    assert actual == expected


def test_if_true():
    expected = "{% if True %}<span>test</span>{% endif %}"

    template = '<span dj-if="True">test</span>'
    actual = convert_template(template)

    assert actual == expected


def test_if_true_internal_tag():
    expected = "<div>{% if True %}<span>test</span>{% endif %}</div>"

    template = '<div><span dj-if="True">test</span></div>'
    actual = convert_template(template)

    assert actual == expected


def test_if_true_initial_attribute_regex(settings):
    settings.ANGLES["initial_attribute_regex"] = r"(:)"

    expected = "{% if True %}<span>test</span>{% endif %}"

    template = '<span :if="True">test</span>'
    actual = convert_template(template)

    assert actual == expected


def test_if_true_initial_attribute_regex_empty(settings):
    settings.ANGLES["initial_attribute_regex"] = r"(?=\w)"

    expected = "{% if True %}<span>test</span>{% endif %}"

    template = '<span if="True">test</span>'
    actual = convert_template(template)

    assert actual == expected


def test_if_with_newlines():
    expected = """
<div class="pt-0{% if True %} pb-0{% endif %}">
    {% if True %}<span>
        test
    </span>{% endif %}
</div>
"""

    template = """
<div class="pt-0{% if True %} pb-0{% endif %}">
    <span dj-if="True">
        test
    </span>
</div>
"""
    actual = convert_template(template)

    assert actual == expected


def test_if_django_variable():
    expected = "<div>{% if some_variable %}<span>test</span>{% endif %}</div>"

    template = '<div><span dj-if="some_variable">test</span></div>'
    actual = convert_template(template)

    assert actual == expected


def test_if_false():
    expected = "<div>{% if False %}<span>test</span>{% endif %}</div>"

    template = "<div><span dj-if='False'>test</span></div>"
    actual = convert_template(template)

    assert actual == expected


def test_elif_else():
    expected = """<h1 class="text-2xl md:text-4xl font-semibold my-4 mb-2">
    {% if is_collection %}<a href="{% url 'movie:collection' slug=collection.slug %}">
    {{ name }}
    </a>
    {% elif name == 'Upcoming' %}<a href="{% url 'movie:upcoming' %}">
    {{ name }}
    </a>
    {% else %}<a href="{% url 'movie:recent' %}">
    {{ name }}
    </a>{% endif %}
</h1>"""

    template = """<h1 class="text-2xl md:text-4xl font-semibold my-4 mb-2">
    <a href="{% url 'movie:collection' slug=collection.slug %}" dj-if="is_collection">
    {{ name }}
    </a>
    <a href="{% url 'movie:upcoming' %}" dj-elif="name == 'Upcoming'">
    {{ name }}
    </a>
    <a href="{% url 'movie:recent' %}" dj-else>
    {{ name }}
    </a>
</h1>"""

    actual = convert_template(template)

    assert actual == expected


def test_multiple_ifs():
    expected = """
{% if is_collection %}<a1 href="{% url 'movie:collection' slug=collection.slug %}">
{{ name }}
</a1>{% endif %}

{% if is_collection %}<a4 href="{% url 'movie:collection' slug=collection.slug %}">
{{ name }}
</a4>{% endif %}
"""

    template = """
<a1 href="{% url 'movie:collection' slug=collection.slug %}" dj-if="is_collection">
{{ name }}
</a1>

<a4 href="{% url 'movie:collection' slug=collection.slug %}" dj-if="is_collection">
{{ name }}
</a4>
"""

    actual = convert_template(template)

    assert actual == expected


def test_multiple_elifs():
    expected = """
{% if is_collection %}<a1 href="{% url 'movie:collection' slug=collection.slug %}">
{{ name }}
</a1>
{% elif name == 'Upcoming' %}<a2 href="{% url 'movie:upcoming' %}">
{{ name }}
</a2>{% endif %}

{% if is_collection %}<a4 href="{% url 'movie:collection' slug=collection.slug %}">
{{ name }}
</a4>
{% elif name == 'Upcoming' %}<a5 href="{% url 'movie:upcoming' %}">
{{ name }}
</a5>{% endif %}
"""

    template = """
<a1 href="{% url 'movie:collection' slug=collection.slug %}" dj-if="is_collection">
{{ name }}
</a1>
<a2 href="{% url 'movie:upcoming' %}" dj-elif="name == 'Upcoming'">
{{ name }}
</a2>

<a4 href="{% url 'movie:collection' slug=collection.slug %}" dj-if="is_collection">
{{ name }}
</a4>
<a5 href="{% url 'movie:upcoming' %}" dj-elif="name == 'Upcoming'">
{{ name }}
</a5>
"""

    actual = convert_template(template)

    assert actual == expected


def test_void_element():
    expected = '{% if is_collection %}<input type="checkbox" checked>{% endif %}'

    template = '<input type="checkbox" checked dj-if="is_collection">'

    actual = convert_template(template)

    assert actual == expected


def test_multiple_void_elements():
    expected = """
{% if is_collection %}<input type="checkbox" checked>{% endif %}

{% if is_collection %}<img src="image.jpg">{% endif %}
"""

    template = """
<input type="checkbox" checked dj-if="is_collection">

<img src="image.jpg" dj-if="is_collection">
"""

    actual = convert_template(template)

    assert actual == expected


def test_multiple_self_closing_elements():
    expected = """
{% if is_collection %}<input type="checkbox" checked />{% endif %}

{% if is_collection %}<img src="image.jpg" />{% endif %}
"""

    template = """
<input type="checkbox" checked dj-if="is_collection" />

<img src="image.jpg" dj-if="is_collection" />
"""

    actual = convert_template(template)

    assert actual == expected


def test_void_element_extra_html():
    expected = '<div>{% if is_collection %}<input type="checkbox" checked>{% endif %}</div>'

    template = '<div><input type="checkbox" checked dj-if="is_collection"></div>'

    actual = convert_template(template)

    assert actual == expected


def test_self_closing_element():
    expected = '{% if is_collection %}<input type="checkbox" checked />{% endif %}'

    template = '<input type="checkbox" checked dj-if="is_collection" />'

    actual = convert_template(template)

    assert actual == expected


def test_if_self_closing_with_right_angle_bracket():
    expected = '{% if is_collection %}<input type="checkbox" class="oh>no" />{% endif %}'

    template = '<input type="checkbox" class="oh>no" dj-if="is_collection" />'

    actual = convert_template(template)

    assert actual == expected


def test_if_void_with_right_angle_bracket():
    expected = '{% if is_collection %}<input type="checkbox" class="oh>no">{% endif %}'

    template = '<input type="checkbox" class="oh>no" dj-if="is_collection">'

    actual = convert_template(template)

    assert actual == expected


def test_if_with_right_angle_bracket():
    expected = '{% if is_collection %}<div class="oh>no"><span>cool</span></div>{% endif %}'

    template = '<div dj-if="is_collection" class="oh>no"><span>cool</span></div>'

    actual = convert_template(template)

    assert actual == expected


def test_elif_with_no_if():
    template = """
<a2 href="{% url 'movie:upcoming' %}" dj-elif="name == 'Upcoming'">
{{ name }}
</a2>
"""

    with pytest.raises(AssertionError) as e:
        convert_template(template)

    assert e.exconly() == "AssertionError: Invalid use of dj-elif outside of a conditional block"


def test_else_with_no_if():
    template = """
<a2 href="{% url 'movie:upcoming' %}" dj-else>
{{ name }}
</a2>
"""

    with pytest.raises(AssertionError) as e:
        convert_template(template)

    assert e.exconly() == "AssertionError: Invalid use of dj-else outside of a conditional block"


def test_extra_else():
    template = """
<a1 href="{% url 'movie:upcoming' %}" dj-if="True">
{{ name }}
</a1>
<a2 href="{% url 'movie:upcoming' %}" dj-else>
{{ name }}
</a2>
<a3 href="{% url 'movie:upcoming' %}" dj-else>
{{ name }}
</a3>
"""

    with pytest.raises(AssertionError) as e:
        convert_template(template)

    assert e.exconly() == "AssertionError: Invalid use of dj-else attribute"


def test_if_component_self_closing():
    expected = "{% if True %}<dj-fake-partial>{% include 'fake-partial.html' %}</dj-fake-partial>{% endif %}"

    template = '<dj-fake-partial dj-if="True" />'
    actual = convert_template(template)

    assert actual == expected


def test_if_component_self_closing_extra_html():
    expected = "<span></span>{% if True %}<dj-fake-partial>{% include 'fake-partial.html' %}</dj-fake-partial>{% endif %}<span></span>"  # noqa: E501

    template = '<span></span><dj-fake-partial dj-if="True" /><span></span>'
    actual = convert_template(template)

    assert actual == expected


def test_if_nested_endif():
    expected = """
{% if movies %}<div>
  {% if True %}<span></span>{% endif %}
</div>
{% else %}<p>
</p>{% endif %}
"""

    template = """
<div dj-if="movies">
  <span dj-if="True"></span dj-endif>
</div>
<p dj-else>
</p>
"""
    actual = convert_template(template)

    assert actual == expected


def test_if_nested_fi():
    expected = """
{% if movies %}<div>
  {% if True %}<span></span>{% endif %}
</div>
{% else %}<p>
</p>{% endif %}
"""

    template = """
<div dj-if="movies">
  <span dj-if="True"></span dj-fi>
</div>
<p dj-else>
</p>
"""
    actual = convert_template(template)

    assert actual == expected


def test_if_elif_nested():
    expected = """
{% if movies %}<div>
  {% if True %}<span></span>
  {% elif True %}<span></span>
  {% elif True %}<span></span>{% endif %}
</div>
{% else %}<p>
</p>{% endif %}
"""

    template = """
<div dj-if="movies">
  <span dj-if="True"></span>
  <span dj-elif="True"></span>
  <span dj-elif="True"></span dj-endif>
</div>
<p dj-else>
</p>
"""
    actual = convert_template(template)

    assert actual == expected


def test_if_nested_same_tag_name():
    expected = """
{% if movies %}<div>
  {% if True %}<div></div>
  {% elif True %}<div></div>
  {% elif True %}<div></div>{% endif %}
</div>
{% else %}<div>
</div>{% endif %}
"""

    template = """
<div dj-if="movies">
  <div dj-if="True"></div>
  <div dj-elif="True"></div>
  <div dj-elif="True"></div dj-endif>
</div>
<div dj-else>
</div>
"""
    actual = convert_template(template)

    assert actual == expected


def test_if_nested():
    expected = """
{% if movies %}<div>
  {% if True %}<span></span>{% endif %}
</div>
{% else %}<p>
</p>{% endif %}
"""

    template = """
<div dj-if="movies">
  <span dj-if="True"></span>
</div>
<p dj-else>
</p>
"""
    actual = convert_template(template)

    assert actual == expected
