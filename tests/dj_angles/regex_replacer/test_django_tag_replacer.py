from collections import namedtuple

import pytest

from dj_angles.regex_replacer import get_django_tag_replacements

# Structure to store parameterize data
Params = namedtuple(
    "Params",
    ("original", "replacement"),
)


@pytest.mark.parametrize(
    Params._fields,
    (
        Params(
            original="{{ var or 'default' }}",
            replacement="{% if var %}{{ var }}{% else %}default{% endif %}",
        ),
        Params(
            original='{{ var or "default" }}',
            replacement="{% if var %}{{ var }}{% else %}default{% endif %}",
        ),
        Params(
            original="{{ var|filter or 'default' }}",
            replacement="{% if var|filter %}{{ var|filter }}{% else %}default{% endif %}",
        ),
        Params(
            original="{{ var1 or var2 }}",
            replacement="{% if var1 %}{{ var1 }}{% else %}{{ var2 }}{% endif %}",
        ),
        Params(
            original="{{ var|default:'default' or 'default' }}",
            replacement="{% if var|default:'default' %}{{ var|default:'default' }}{% else %}default{% endif %}",
        ),
    ),
)
def test_or(original, replacement):
    replacements = get_django_tag_replacements(original)
    assert len(replacements) == 1

    for tag_replacement in replacements:
        assert tag_replacement.original == original
        assert tag_replacement.replacement == replacement


@pytest.mark.parametrize(
    Params._fields,
    (
        Params(
            original="{{ 'true' if var else 'false' }}",
            replacement="{% if var %}true{% else %}false{% endif %}",
        ),
        Params(
            original='{{ "true" if var else "false" }}',
            replacement="{% if var %}true{% else %}false{% endif %}",
        ),
        Params(
            original="{{ 'true' if var|filter else 'false' }}",
            replacement="{% if var|filter %}true{% else %}false{% endif %}",
        ),
        Params(
            original="{{ var2 if var1 else var3 }}",
            replacement="{% if var1 %}{{ var2 }}{% else %}{{ var3 }}{% endif %}",
        ),
        Params(
            original="{{ 1 if var else 2 }}",
            replacement="{% if var %}{{ 1 }}{% else %}{{ 2 }}{% endif %}",
        ),
        Params(
            original="{{ True if var else False }}",
            replacement="{% if var %}{{ True }}{% else %}{{ False }}{% endif %}",
        ),
        Params(
            original="{{ 'a'|upper if cond else 'b'|lower }}",
            replacement="{% if cond %}{{ 'a'|upper }}{% else %}{{ 'b'|lower }}{% endif %}",
        ),
        Params(
            original="{{ var2|default:'x' if cond else var3|default:'y' }}",
            replacement="{% if cond %}{{ var2|default:'x' }}{% else %}{{ var3|default:'y' }}{% endif %}",
        ),
        Params(
            original="{{ 'a'|upper if cond else 'b'|lower }}",
            replacement="{% if cond %}{{ 'a'|upper }}{% else %}{{ 'b'|lower }}{% endif %}",
        ),
        Params(
            original="{{ var2|default:'x' if cond else var3|default:'y' }}",
            replacement="{% if cond %}{{ var2|default:'x' }}{% else %}{{ var3|default:'y' }}{% endif %}",
        ),
        Params(
            original="{{  'yes'   if   var   else   'no'  }}",
            replacement="{% if var %}yes{% else %}no{% endif %}",
        ),
        Params(
            original="{{ var2|lower if var1 else var3|upper }}",
            replacement="{% if var1 %}{{ var2|lower }}{% else %}{{ var3|upper }}{% endif %}",
        ),
    ),
)
def test_inline_if(original, replacement):
    replacements = get_django_tag_replacements(original)
    assert len(replacements) == 1

    for tag_replacement in replacements:
        assert tag_replacement.original == original
        assert tag_replacement.replacement == replacement


@pytest.mark.parametrize(
    "original",
    (
        "{{ 'x' if var }}",  # missing else
        "{{ 'x' else 'y' }}",  # missing if
        "{{ if var else 'y' }}",  # invalid pythonic ternary
        "{{ 'if' in str }}",  # contains 'if' in expression but not ternary
        "{{ \"'if' in str\" }}",  # quoted string containing 'if'
        "{{ '{{ x }}' if cond else 'y' }}",  # braces inside quoted branch value
        "{{ 'x' if cond else '{{ y }}' }}",  # braces inside quoted branch value
        "{{ var or '{{ x }}' }}",  # braces in default value
    ),
)
def test_negative_non_matching(original):
    replacements = get_django_tag_replacements(original)
    assert len(replacements) == 0


def test_or_with_quotes():
    actual = get_django_tag_replacements("{{ 'a or b' }}")
    assert len(actual) == 0

    actual = get_django_tag_replacements('{{ "a or b" }}')
    assert len(actual) == 0
