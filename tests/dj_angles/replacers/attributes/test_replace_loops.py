from collections import namedtuple

import pytest

from dj_angles.replacers.attributes import replace_loops

Params = namedtuple(
    "Params",
    ("original", "replacement"),
)


@pytest.mark.parametrize(
    Params._fields,
    (
        # Self-closing element
        Params(
            original="<li dj-for='i in items' />",
            replacement="{% for i in items %}<li></li>{% endfor %}",
        ),
        # Self-closing with double quotes
        Params(
            original='<li dj-for="i in items" />',
            replacement="{% for i in items %}<li></li>{% endfor %}",
        ),
        # Element with children
        Params(
            original="<li dj-for='i in items'><span>{{ i }}</span></li>",
            replacement="{% for i in items %}<li><span>{{ i }}</span></li>{% endfor %}",
        ),
        # Explicit dj-endfor on closing tag
        Params(
            original="<li dj-for='i in items'><span>{{ i }}</span></li dj-endfor>",
            replacement="{% for i in items %}<li><span>{{ i }}</span></li>{% endfor %}",
        ),
        # With dj-empty sibling
        Params(
            original="<li dj-for='i in items'>{{ i }}</li><li dj-empty>No items</li>",
            replacement="{% for i in items %}<li>{{ i }}</li>{% empty %}<li>No items</li>{% endfor %}",
        ),
        # Void element (img)
        Params(
            original="<img dj-for='i in items' />",
            replacement="{% for i in items %}<img></img>{% endfor %}",
        ),
    ),
)
def test_replace_loops(original, replacement):
    actual = replace_loops(original)
    assert actual == replacement


def test_nested_loops():
    original = "<tr dj-for='row in rows'><td dj-for='cell in row'>{{ cell }}</td></tr>"
    expected = "{% for row in rows %}<tr>{% for cell in row %}<td>{{ cell }}</td>{% endfor %}</tr>{% endfor %}"
    actual = replace_loops(original)
    assert actual == expected


def test_missing_expression_raises():
    with pytest.raises(AssertionError, match="dj-for attribute must have a value"):
        replace_loops("<li dj-for></li>")


def test_unquoted_expression_raises():
    with pytest.raises(AssertionError, match="dj-for attribute value must be quoted"):
        replace_loops("<li dj-for=i_in_items />")


def test_orphaned_empty_raises():
    with pytest.raises(AssertionError, match="Invalid use of dj-empty attribute without a preceding dj-for"):
        replace_loops("<li dj-empty>No items</li>")


def test_with_value():
    """dj-for + dj-value on the same self-closing element should compose correctly after
    replace_loops runs (dj-value is handled by the subsequent replace_values pass)."""
    original = "<li dj-for='i in items' dj-value='i' />"
    # After replace_loops, dj-for is resolved; dj-value remains for replace_values
    result = replace_loops(original)
    assert result.startswith("{% for i in items %}")
    assert "dj-value" in result
    assert result.endswith("{% endfor %}")


def test_with_value_double():
    """dj-for + dj-value on the same self-closing element should compose correctly after
    replace_loops runs (dj-value is handled by the subsequent replace_values pass)."""
    original = '<li dj-for="i in items" dj-value="i" />'
    # After replace_loops, dj-for is resolved; dj-value remains for replace_values
    result = replace_loops(original)
    assert result.startswith("{% for i in items %}")
    assert "dj-value" in result
    assert result.endswith("{% endfor %}")


def test_no_loops_is_noop():
    original = "<div><p>Hello</p></div>"
    assert replace_loops(original) == original
