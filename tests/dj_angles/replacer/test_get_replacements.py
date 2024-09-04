from collections import namedtuple

import pytest

from dj_angles.replacer import get_replacements

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


@pytest.mark.parametrize(
    ReplacementParams._fields,
    (
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
    ),
)
def test_typical(template_string, replacement_string):
    expected = [
        (template_string, replacement_string),
    ]
    actual = get_replacements(template_string)

    assert actual == expected


@pytest.mark.parametrize(
    ReplacementParams._fields,
    (
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
    ),
)
def test_custom_initial_tag_regex(template_string, replacement_string, settings):
    settings.ANGLES = {"initial_tag_regex": r"(dj-|\$)"}

    expected = [
        (template_string, replacement_string),
    ]
    actual = get_replacements(template_string)

    assert actual == expected


@pytest.mark.parametrize(
    ReplacementParams._fields,
    (
        ReplacementParams(
            template_string="<partial />",
            replacement_string="{% include 'partial.html' %}",
        ),
    ),
)
def test_initial_tag_regex_empty_string(template_string, replacement_string, settings):
    settings.ANGLES = {"initial_tag_regex": ""}

    expected = [
        (template_string, replacement_string),
    ]
    actual = get_replacements(template_string)

    assert actual == expected


@pytest.mark.parametrize(
    ReplacementParams._fields,
    (
        ReplacementParams(
            template_string="<partial />",
            replacement_string="{% include 'partial.html' %}",
        ),
    ),
)
def test_initial_tag_regex_none(template_string, replacement_string, settings):
    settings.ANGLES = {"initial_tag_regex": None}

    expected = [
        (template_string, replacement_string),
    ]
    actual = get_replacements(template_string)

    assert actual == expected


@pytest.mark.parametrize(
    ReplacementParams._fields,
    (
        ReplacementParams(
            template_string="<Partial />",
            replacement_string="{% include 'partial.html' %}",
        ),
    ),
)
def test_initial_tag_regex_lower_case_tag(template_string, replacement_string, settings):
    settings.ANGLES = {"initial_tag_regex": None, "lower_case_tag": True}

    expected = [
        (template_string, replacement_string),
    ]
    actual = get_replacements(template_string)

    assert actual == expected


@pytest.mark.parametrize(
    ReplacementParams._fields,
    (
        ReplacementParams(
            template_string="<blob 'partial.html' />",
            replacement_string="{% include 'partial.html' %}",
        ),
    ),
)
def test_mappers_string(template_string, replacement_string, settings):
    settings.ANGLES = {
        "initial_tag_regex": None,
        "mappers": {
            "blob": "include",
        },
    }

    expected = [
        (template_string, replacement_string),
    ]
    actual = get_replacements(template_string)

    assert actual == expected


@pytest.mark.parametrize(
    ReplacementParams._fields,
    (
        ReplacementParams(
            template_string="<blob />",
            replacement_string="blob2",
        ),
    ),
)
def test_mappers_callable(template_string, replacement_string, settings):
    settings.ANGLES = {
        "initial_tag_regex": None,
        "mappers": {"blob": lambda component_name, template_tag_args, is_tag_closing: "blob2"},
    }

    expected = [
        (template_string, replacement_string),
    ]
    actual = get_replacements(template_string)

    assert actual == expected
