from collections import namedtuple

import pytest

from dj_angles.regex_replacer import get_attribute_replacements

# Structure to store parameterize data
Params = namedtuple(
    "Params",
    ("original", "replacement"),
)


@pytest.mark.parametrize(
    Params._fields,
    (
        Params(
            original="<img src='partial.png' dj-if='True' />",
            replacement="{% if True %}<img src='partial.png' />{% endif %}",
        ),
    ),
)
def test_if(original, replacement):
    actual = get_attribute_replacements(original)

    for tag_replacement in actual:
        assert tag_replacement.original == original
        assert tag_replacement.replacement == replacement
