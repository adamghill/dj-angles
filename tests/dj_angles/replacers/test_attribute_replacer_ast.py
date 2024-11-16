"""Test for AST-based attribute replacer."""

import pytest

from dj_angles.replacers.attribute_replacer_ast import get_attribute_replacements_ast


def test_simple_if():
    """Test simple dj-if replacement."""
    html = '<span dj-if="True">test</span>'
    replacements = get_attribute_replacements_ast(html)

    assert len(replacements) == 1
    r = replacements[0]
    print(f"Original: {r.original}")
    print(f"Replacement: {r.replacement}")

    # Should wrap with {% if %} and {% endif %}
    assert "{% if True %}" in r.replacement
    assert "{% endif %}" in r.replacement
    assert "dj-if" not in r.replacement


def test_nested_same_tag():
    """Test the bug case: nested dj-if/dj-else with same tag names."""
    html = """<div dj-if="outer">
  <div dj-if="inner">
    <p>Inner true</p>
  </div>
  <div dj-else>
    <p>Inner false</p>
  </div>
</div>
<div dj-else>
  <p>Outer false</p>
</div>"""

    replacements = get_attribute_replacements_ast(html)

    print(f"\nFound {len(replacements)} replacements:")
    for i, r in enumerate(replacements):
        print(f"\n{i}. Original: {r.original[:50]}...")
        print(f"   Replacement: {r.replacement[:50]}...")

    assert len(replacements) == 4

    # Check that we have proper if/else structure
    # Outer if
    outer_if = replacements[0]
    assert "{% if outer %}" in outer_if.replacement

    # Inner if
    inner_if = replacements[1]
    assert "{% if inner %}" in inner_if.replacement

    # Inner else
    inner_else = replacements[2]
    assert "{% else %}" in inner_else.replacement

    # Outer else
    outer_else = replacements[3]
    assert "{% else %}" in outer_else.replacement


if __name__ == "__main__":
    test_simple_if()
    test_nested_same_tag()
    print("\nAll tests passed!")
