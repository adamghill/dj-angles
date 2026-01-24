from collections import namedtuple

import pytest

from dj_angles.replacers.variables import replace_variables

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
    actual = replace_variables(original)
    assert actual == replacement


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
    actual = replace_variables(original)
    assert actual == replacement


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
    actual = replace_variables(original)
    assert actual == original


def test_or_with_quotes():
    actual = replace_variables("{{ 'a or b' }}")
    assert actual == "{{ 'a or b' }}"

    actual = replace_variables('{{ "a or b" }}')
    assert actual == '{{ "a or b" }}'


@pytest.mark.parametrize(
    Params._fields,
    (
        Params(
            original="{{ 'if' if cond else 'else' }}",
            replacement="{% if cond %}if{% else %}else{% endif %}",
        ),
        Params(
            original='{{ "if" if cond else "else" }}',
            replacement="{% if cond %}if{% else %}else{% endif %}",
        ),
        Params(
            original="{{ 'or' or 'else' }}",
            replacement="{% if 'or' %}{{ 'or' }}{% else %}else{% endif %}",
        ),
        Params(
            original="{{ 'this or that' or 'default' }}",
            replacement="{% if 'this or that' %}{{ 'this or that' }}{% else %}default{% endif %}",
        ),
        Params(
            original="{{ 'A if B else C' if cond else 'D' }}",
            replacement="{% if cond %}A if B else C{% else %}D{% endif %}",
        ),
        Params(
            original="{{ var or 'default with or' }}",
            replacement="{% if var %}{{ var }}{% else %}default with or{% endif %}",
        ),
        Params(
            original="{{ 'ends with or' or default }}",
            replacement="{% if 'ends with or' %}{{ 'ends with or' }}{% else %}{{ default }}{% endif %}",
        ),
    ),
)
def test_stress_cases(original, replacement):
    actual = replace_variables(original)
    assert actual == replacement
