from collections import namedtuple

import pytest

from dj_angles.replacers.attributes import replace_attributes

# Structure to store parameterize data
Params = namedtuple(
    "Params",
    ("original", "replacement"),
)


@pytest.mark.parametrize(
    Params._fields,
    (
        Params(
            original="<div dj-if='condition'>content</div>",
            replacement="{% if condition %}<div>content</div>{% endif %}",
        ),
        Params(
            original="<div dj-if='condition'>content</div>",
            replacement="{% if condition %}<div>content</div>{% endif %}",
        ),
        Params(
            original="<div dj-if='condition'>content<span dj-if='inner'>inner</span></div>",
            replacement="{% if condition %}<div>content{% if inner %}<span>inner</span>{% endif %}</div>{% endif %}",
        ),
        Params(
            original=("<div dj-if='c1'>1</div><div dj-elif='c2'>2</div><div dj-else>3</div>"),
            replacement=("{% if c1 %}<div>1</div>{% elif c2 %}<div>2</div>{% else %}<div>3</div>{% endif %}"),
        ),
        Params(
            original=("<div dj-if='c1'>1</div><div dj-else>2</div>"),
            replacement=("{% if c1 %}<div>1</div>{% else %}<div>2</div>{% endif %}"),
        ),
        Params(
            original="<div dj-if='c1'>1</div><span dj-if='c2'>2</span>",
            replacement="{% if c1 %}<div>1</div>{% endif %}{% if c2 %}<span>2</span>{% endif %}",
        ),
        Params(
            original="<div dj-if='c1'><span dj-if='c2'>2</span></div><div dj-else>3</div>",
            replacement="{% if c1 %}<div>{% if c2 %}<span>2</span>{% endif %}</div>{% else %}<div>3</div>{% endif %}",
        ),
        # Attribute variations
        Params(
            original='<div dj-if="condition">content</div>',
            replacement="{% if condition %}<div>content</div>{% endif %}",
        ),
        Params(
            original="<div dj-if=condition>content</div>",
            replacement="{% if condition %}<div>content</div>{% endif %}",
        ),
        # dj-endif
        Params(
            original="<div dj-if='c'>content</div dj-endif>",
            replacement="{% if c %}<div>content</div>{% endif %}",
        ),
        Params(
            original="<div dj-if='c'>content</div dj-fi>",
            replacement="{% if c %}<div>content</div>{% endif %}",
        ),
        # Self-closing
        Params(
            original="<img dj-if='c' />",
            replacement="{% if c %}<img />{% endif %}",
        ),
        Params(
            original="<img dj-if='c1' /><img dj-else />",
            replacement="{% if c1 %}<img />{% else %}<img />{% endif %}",
        ),
    ),
)
def test_attributes(original, replacement):
    actual = replace_attributes(original)
    assert actual == replacement


def test_orphaned_else():
    with pytest.raises(AssertionError, match="Invalid use of dj-else attribute"):
        replace_attributes("<div dj-else>orphaned</div>")

    with pytest.raises(AssertionError, match="Invalid use of dj-elif attribute"):
        replace_attributes("<div dj-elif='c'>orphaned</div>")
