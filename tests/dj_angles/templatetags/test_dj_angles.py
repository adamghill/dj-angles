import pytest
from django.template import Context, Template
from example.book.models import Book


def test_call_tag():
    def some_function():
        return "expected output"

    template = Template("""
{% call some_function as result %}

{{ result }}
""")
    context = Context({"some_function": some_function})
    rendered = template.render(context)

    assert "expected output" in rendered


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
