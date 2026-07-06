from collections import namedtuple

import pytest

from dj_angles.replacers.attributes import replace_values

# Structure to store parameterize data
Params = namedtuple(
    "Params",
    ("original", "replacement"),
)


@pytest.mark.parametrize(
    Params._fields,
    (
        Params(
            original="<div dj-value='request.user'></div>",
            replacement="<div>{{ request.user }}</div>",
        ),
        Params(
            original='<div dj-value="request.user"></div>',
            replacement="<div>{{ request.user }}</div>",
        ),
        Params(
            original="<div dj-value='x'>fallback</div>",
            replacement="<div>{{ x }}</div>",
        ),
        Params(
            original="<div dj-value='user.name|upper'></div>",
            replacement="<div>{{ user.name|upper }}</div>",
        ),
        Params(
            original="<img dj-value='x' />",
            replacement="<img>{{ x }}</img>",
        ),
        Params(
            original="<input dj-value='x'>",
            replacement="<input>{{ x }}</input>",
        ),
        Params(
            original='<div class="foo" dj-value="x"></div>',
            replacement='<div class="foo">{{ x }}</div>',
        ),
        Params(
            original="<div dj-value='x'><span>nested</span></div>",
            replacement="<div>{{ x }}</div>",
        ),
        Params(
            original="<div dj-value='x'>  <span>nested</span>  </div>",
            replacement="<div>{{ x }}</div>",
        ),
    ),
)
def test_replace_values(original, replacement):
    actual = replace_values(original)
    assert actual == replacement


def test_empty_value_raises():
    with pytest.raises(AssertionError, match="dj-value attribute must have a value"):
        replace_values("<div dj-value=''></div>")


def test_missing_value_raises():
    with pytest.raises(AssertionError, match="dj-value attribute must have a value"):
        replace_values("<div dj-value></div>")


def test_unquoted_value_raises():
    with pytest.raises(AssertionError, match="dj-value attribute value must be quoted"):
        replace_values("<div dj-value=x></div>")


def test_closing_tag_raises():
    with pytest.raises(AssertionError, match="Invalid use of dj-value attribute on closing tag"):
        replace_values("</div dj-value='x'>")


def test_multiple_elements():
    original = "<div dj-value='x'></div><span dj-value='y'></span>"
    expected = "<div>{{ x }}</div><span>{{ y }}</span>"

    actual = replace_values(original)

    assert actual == expected


def test_nested_elements():
    original = "<div dj-value='outer'><span dj-value='inner'></span></div>"
    expected = "<div>{{ outer }}</div>"

    actual = replace_values(original)

    assert actual == expected
