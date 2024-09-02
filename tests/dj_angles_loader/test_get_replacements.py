from collections import namedtuple

import pytest

from dj_angles.template_loader import get_replacements

# Structure to store parameterize data
ReplacementParams = namedtuple(
    "ReplacementParams",
    (
        "template_string",
        "replacement_string",
    ),
)


def _shadowify(s: str) -> str:
    return f"<template shadowrootmode='open'>{s}</template>"


replacement_params = (
    ReplacementParams(
        template_string="<dj-extends 'base.html' />",
        replacement_string="{% extends 'base.html' %}",
    ),
    ReplacementParams(
        template_string="<dj-include 'partial.html' />",
        replacement_string="{% include 'partial.html' %}",
    ),
    ReplacementParams(
        template_string="<dj-include 'partial.html' shadow />",
        replacement_string=_shadowify("{% include 'partial.html' %}"),
    ),
    ReplacementParams(
        template_string="<dj-partial />",
        replacement_string="{% include 'partial.html' %}",
    ),
    ReplacementParams(
        template_string="<$partial />",
        replacement_string="{% include 'partial.html' %}",
    ),
    ReplacementParams(
        template_string="<$partial! />",
        replacement_string=_shadowify("{% include 'partial.html' %}"),
    ),
    ReplacementParams(
        template_string="<$partial!>",
        replacement_string="<template shadowrootmode='open'>{% include 'partial.html' %}",
    ),
    ReplacementParams(
        template_string="</$partial!>",
        replacement_string="</template>",
    ),
    ReplacementParams(
        template_string="<$directory/partial />",
        replacement_string="{% include 'directory/partial.html' %}",
    ),
    ReplacementParams(
        template_string="<dj-comment>",
        replacement_string="{% comment %}",
    ),
    ReplacementParams(
        template_string="</dj-comment>",
        replacement_string="{% endcomment %}",
    ),
    ReplacementParams(
        template_string="<dj-#>",
        replacement_string="{% comment %}",
    ),
    ReplacementParams(
        template_string="</dj-#>",
        replacement_string="{% endcomment %}",
    ),
    ReplacementParams(
        template_string="<dj-verbatim>",
        replacement_string="{% verbatim %}",
    ),
    ReplacementParams(
        template_string="</dj-verbatim>",
        replacement_string="{% endverbatim %}",
    ),
    ReplacementParams(
        template_string="<dj-autoescape-on>",
        replacement_string="{% autoescape on %}",
    ),
    ReplacementParams(
        template_string="</dj-autoescape-on>",
        replacement_string="{% endautoescape %}",
    ),
    ReplacementParams(
        template_string="</dj-autoescape-off>",
        replacement_string="{% endautoescape %}",
    ),
    ReplacementParams(
        template_string="<dj-csrf />",
        replacement_string="{% csrf_token %}",
    ),
    ReplacementParams(
        template_string="<dj-csrf-input />",
        replacement_string="{% csrf_token %}",
    ),
    ReplacementParams(
        template_string="<dj-block>",
        replacement_string="{% block %}",
    ),
    ReplacementParams(
        template_string="<dj-block content>",
        replacement_string="{% block content %}",
    ),
    ReplacementParams(
        template_string="</dj-block>",
        replacement_string="{% endblock %}",
    ),
    ReplacementParams(
        template_string="</dj-block content>",
        replacement_string="{% endblock content %}",
    ),
)


@pytest.mark.parametrize(ReplacementParams._fields, replacement_params)
def test_replacements(template_string, replacement_string):
    expected = [
        (template_string, replacement_string),
    ]
    actual = get_replacements(template_string)

    assert actual == expected
