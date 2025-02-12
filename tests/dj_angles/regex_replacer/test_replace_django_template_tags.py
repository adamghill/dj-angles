import pytest

from dj_angles.exceptions import InvalidEndTagError
from dj_angles.regex_replacer import (
    end_of_tag_index,
    get_end_of_attribute_value,
    get_previous_element_tag,
    replace_django_template_tags,
)


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


def test_short_include_self_closing_shadow_bang():
    expected = "<dj-partial><template shadowrootmode='open'>{% include 'partial.html' %}</template></dj-partial>"

    template = "<dj-partial! />"
    actual = replace_django_template_tags(template)

    assert actual == expected


def test_short_include_self_closing_shadow():
    expected = "<dj-partial><template shadowrootmode='open'>{% include 'partial.html' %}</template></dj-partial>"

    template = "<dj-include template='partial.html' shadow />"
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


def test_include_arguments_with_newlines():
    expected = "<dj-partial>{% include 'partial.html' with blob=True stuff=True %}</dj-partial>"

    template = """<dj-partial with blob=True
stuff=True></dj-partial>"""
    actual = replace_django_template_tags(template)

    assert actual == expected


def test_include_arguments_with_newlines_and_extra_spaces():
    expected = "<dj-partial>{% include 'partial.html' with blob=True stuff=True %}</dj-partial>"

    template = """<dj-partial with blob=True
    stuff=True></dj-partial>"""
    actual = replace_django_template_tags(template)

    assert actual == expected


def test_include_arguments_with_newlines_and_tab():
    expected = "<dj-partial>{% include 'partial.html' with blob=True stuff=True %}</dj-partial>"

    template = """<dj-partial with blob=True
	stuff=True></dj-partial>"""
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


def test_with():
    expected = '<dj-www-components-include>{% include "www/components/include.html" with request=request only %}\
</dj-www-components-include>'

    template = '<dj-include src="www/components/include.html" with request=request only></dj-include>'
    actual = replace_django_template_tags(template)

    assert actual == expected


def test_with_only():
    expected = '<dj-www-components-include>{% include "www/components/include.html" with request=request %}\
</dj-www-components-include>'

    template = '<dj-include src="www/components/include.html" with request=request></dj-include>'
    actual = replace_django_template_tags(template)

    assert actual == expected


def test_if_true():
    expected = "<div>{% if True %}<span>test</span>{% endif %}</div>"

    template = '<div><span dj-if="True">test</span></div>'
    actual = replace_django_template_tags(template)

    assert actual == expected


def test_if_true_2():
    expected = "{% if True %}<span>test</span>{% endif %}"

    template = '<span dj-if="True">test</span>'
    actual = replace_django_template_tags(template)

    assert actual == expected


def test_if_blob():
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
    actual = replace_django_template_tags(template)

    assert actual == expected


def test_if_django_variable():
    expected = "<div>{% if some_variable %}<span>test</span>{% endif %}</div>"

    template = '<div><span dj-if="some_variable">test</span></div>'
    actual = replace_django_template_tags(template)

    assert actual == expected


def test_if_false():
    expected = "<div>{% if False %}<span>test</span>{% endif %}</div>"

    template = '<div><span dj-if="False">test</span></div>'
    actual = replace_django_template_tags(template)

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

    actual = replace_django_template_tags(template)

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

    actual = replace_django_template_tags(template)

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

    actual = replace_django_template_tags(template)

    assert actual == expected


def test_elif_with_no_if():
    template = """
<a2 href="{% url 'movie:upcoming' %}" dj-elif="name == 'Upcoming'">
{{ name }}
</a2>
"""

    with pytest.raises(AssertionError) as e:
        replace_django_template_tags(template)

    assert e.exconly() == "AssertionError: Invalid use of dj-elif outside of a conditional block"


def test_else_with_no_if():
    template = """
<a2 href="{% url 'movie:upcoming' %}" dj-else>
{{ name }}
</a2>
"""

    with pytest.raises(AssertionError) as e:
        replace_django_template_tags(template)

    assert e.exconly() == "AssertionError: Invalid use of dj-else outside of a conditional block"


def test_extra_else():
    template = """
<a1 href="{% url 'movie:upcoming' %}" dj-id="True">
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
        replace_django_template_tags(template)

    assert e.exconly() == "AssertionError: Invalid use of dj-else outside of a conditional block"


def test_get_end_of_attribute_value():
    assert get_end_of_attribute_value('"hello"', 0) == ("hello", 7)
    assert get_end_of_attribute_value('dj-if="hello"', 6) == ("hello", 13)
    assert get_end_of_attribute_value("dj-if='hello'", 6) == ("hello", 13)
    assert get_end_of_attribute_value("dj-if=hello", 6) == ("hello", 11)
    assert get_end_of_attribute_value("dj-if=hello there", 6) == ("hello", 11)
    assert get_end_of_attribute_value("dj-if=hello.there", 6) == ("hello.there", 17)
    assert get_end_of_attribute_value("dj-if=hello><span></span>", 6) == ("hello", 11)


def test_get_previous_element_tag():
    assert get_previous_element_tag("<div dj-if='hello'>test</div>", 4) == ("div", 0)
    assert get_previous_element_tag("<span dj-if=hello>test</div>", 5) == ("span", 0)
    assert get_previous_element_tag("<p dj-if=hello there>test</div>", 2) == ("p", 0)
    assert get_previous_element_tag("<div dj-if=hello.there>test</div>", 4) == ("div", 0)
    assert get_previous_element_tag("<div><div dj-if=hello.there>test</div></div>", 10) == ("div", 5)


def test_end_of_tag_index():
    assert end_of_tag_index("<div dj-if='hello'>test</div>", 4, "div") == 29
    assert end_of_tag_index("<div dj-if='hello'><div>test</div></div>", 4, "div") == 40
    assert end_of_tag_index("<div dj-if='hello'><div>test</div></div>", 20, "div") == 34
    assert end_of_tag_index("<div dj-if='hello'><span>test</span></div>", 20, "div") == 42

    expected = 61
    html = """
<div dj-if='hello'>
    <div>
        test
    </div>
</div><div><p>hello</p></div>"""
    actual = end_of_tag_index(html, 4, "div")
    assert actual == expected

    assert end_of_tag_index("<img dj-if='hello' />", 4, "img") == 21
    assert end_of_tag_index("<img dj-if='hello'>", 4, "img") == 19
