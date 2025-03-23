import pytest
from django.template import Context, Template
from example.book.models import Book


def test_call_tag_with_context_variable():
    template = Template("""
{% call some_function as result %}

{{ result }}
""")
    context = Context({"some_function": lambda: "expected output"})
    rendered = template.render(context)

    assert "expected output" in rendered


def test_call_tag_with_context_variable_no_output():
    template = Template("""
{% call some_function as result %}
""")
    context = Context({"some_function": lambda: "expected output"})
    rendered = template.render(context)

    assert "expected output" not in rendered


def test_call_tag():
    template = Template("""
{% call some_function %}
""")
    context = Context({"some_function": lambda: "expected output"})
    rendered = template.render(context)

    assert "expected output" in rendered


def test_call_tag_obj():
    template = Template("""
{% call some_function %}
""")
    context = Context({"some_function": lambda: 123})
    rendered = template.render(context)

    assert "123" in rendered


@pytest.mark.django_db
def test_model_tag():
    Book.objects.create(id=1, title="Huckleberry Finn")

    template = Template("""
{% model Book.objects.filter(id=1).first() as book %}

{{ book.title }}
""")
    context = Context({"Book": Book})
    rendered = template.render(context)

    assert "Huckleberry Finn" in rendered
