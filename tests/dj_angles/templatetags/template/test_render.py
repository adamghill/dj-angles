import pytest
from django.template import Context, Template
from django.template.exceptions import TemplateSyntaxError


def test_template_tag():
    template = Template("""
{% template partial() %}
this is a template
{% endtemplate %}

{% call partial() %}
""")
    context = Context({})
    rendered = template.render(context)

    assert "this is a template" in rendered


def test_template_tag_arg():
    template = Template("""
{% template partial(name) %}
this is a template -> {{ name }}
{% endtemplate %}

{% call partial('test1') %}
""")
    context = Context({})
    rendered = template.render(context)

    assert "this is a template -> test1" in rendered


def test_template_tag_context():
    template = Template("""
{% template partial(name) %}
this is a template -> {{ name }}
{% endtemplate %}

{% call partial(test1) %}
""")
    context = Context({"test1": "test2"})
    rendered = template.render(context)

    assert "this is a template -> test2" in rendered


def test_template_tag_context_conflict():
    template = Template("""
{% template partial(name) %}
this is a template -> {{ name }}
{% endtemplate %}

{% call partial('test2') %}
""")
    context = Context({"name": "test1"})
    rendered = template.render(context)

    assert "this is a template -> test2" in rendered


def test_template_tag_missing_arg():
    template = Template("""
{% template partial(name) %}
this is a template -> {{ name }}
{% endtemplate %}

{% call partial() %}
""")

    with pytest.raises(TemplateSyntaxError) as e:
        template.render(Context({}))

    assert e.exconly() == "django.template.exceptions.TemplateSyntaxError: Invalid number of arguments"


def test_template_tag_default_kwarg():
    template = Template("""
{% template partial(name='test1') %}
this is a template -> {{ name }}
{% endtemplate %}

{% call partial() %}
""")

    context = Context({})
    rendered = template.render(context)

    assert "this is a template -> test1" in rendered


def test_template_tag_default_kwarg_from_context():
    template = Template("""
{% template partial(name=test1) %}
this is a template -> {{ name }}
{% endtemplate %}

{% call partial() %}
""")

    context = Context({"test1": "test2"})
    rendered = template.render(context)

    assert "this is a template -> test2" in rendered


def test_template_tag_kwarg_override():
    template = Template("""
{% template partial(name=test1) %}
this is a template -> {{ name }}
{% endtemplate %}

{% call partial(name='test3') %}
""")

    context = Context({"test1": "test2"})
    rendered = template.render(context)

    assert "this is a template -> test3" in rendered


def test_template_tag_kwarg_from_context():
    template = Template("""
{% template partial(name=test1) %}
this is a template -> {{ name }}
{% endtemplate %}

{% call partial(name=test3) %}
""")

    context = Context({"test1": "test2", "test3": "test4"})
    rendered = template.render(context)

    assert "this is a template -> test4" in rendered


def test_template_tag_template_with_context():
    template = Template("""
{% template partial() with context %}
this is a template -> {{ name }}
{% endtemplate %}

{% call partial() %}
""")

    context = Context({"name": "test1"})
    rendered = template.render(context)

    assert "this is a template -> test1" in rendered


def test_template_tag_template_without_context():
    template = Template("""
{% template partial() %}
this is a template -> ={{ name }}=
{% endtemplate %}

{% call partial() %}
""")

    context = Context({"name": "test1"})
    rendered = template.render(context)

    assert "this is a template -> ==" in rendered
