from collections import namedtuple

import pytest

from dj_angles.mappers.mapper import clear_tag_map
from dj_angles.regex_replacer import get_tag_replacements

# Structure to store parameterize data
Params = namedtuple(
    "Params",
    ("original", "replacement"),
)


def _shadowify(s: str) -> str:
    return f"<dj-partial><template shadowrootmode='open'>{s}</template></dj-partial>"


@pytest.mark.parametrize(
    Params._fields,
    (
        Params(
            original="<dj-extends 'base.html' />",
            replacement="{% extends 'base.html' %}",
        ),
        Params(
            original="<dj-extends parent='base.html' />",
            replacement="{% extends 'base.html' %}",
        ),
        Params(
            original="<dj-include 'partial.html' />",
            replacement="<dj-partial>{% include 'partial.html' %}</dj-partial>",
        ),
        Params(
            original="<dj-include 'partial.html' shadow />",
            replacement=_shadowify("{% include 'partial.html' %}"),
        ),
        Params(
            original="<dj-include 'partial.html' test='hello' />",
            replacement="<dj-partial>{% include 'partial.html' test='hello' %}</dj-partial>",
        ),
        Params(
            original="<dj-include 'shadow-partial.html' />",
            replacement="<dj-shadow-partial>{% include 'shadow-partial.html' %}</dj-shadow-partial>",
        ),
        Params(
            original="<dj-partial />",
            replacement="<dj-partial>{% include 'partial.html' %}</dj-partial>",
        ),
        Params(
            original="<dj-partial test='hello' />",
            replacement="<dj-partial>{% include 'partial.html' test='hello' %}</dj-partial>",
        ),
        Params(
            original="<dj-shadow-partial />",
            replacement="<dj-shadow-partial>{% include 'shadow-partial.html' %}</dj-shadow-partial>",
        ),
        Params(
            original="<dj-comment>",
            replacement="{% comment %}",
        ),
        Params(
            original="</dj-comment>",
            replacement="{% endcomment %}",
        ),
        Params(
            original="<dj-#>",
            replacement="{% comment %}",
        ),
        Params(
            original="</dj-#>",
            replacement="{% endcomment %}",
        ),
        Params(
            original="<dj-verbatim>",
            replacement="{% verbatim %}",
        ),
        Params(
            original="</dj-verbatim>",
            replacement="{% endverbatim %}",
        ),
        Params(
            original="<dj-autoescape-on>",
            replacement="{% autoescape on %}",
        ),
        Params(
            original="</dj-autoescape-on>",
            replacement="{% endautoescape %}",
        ),
        Params(
            original="</dj-autoescape-off>",
            replacement="{% endautoescape %}",
        ),
        Params(
            original="<dj-csrf />",
            replacement="{% csrf_token %}",
        ),
        Params(
            original="<dj-csrf-input />",
            replacement="{% csrf_token %}",
        ),
        Params(
            original="<dj-block name='content'>",
            replacement="{% block content %}",
        ),
        Params(
            original="</dj-block name='content'>",
            replacement="{% endblock content %}",
        ),
        Params(
            original="<dj-block 'content'>",
            replacement="{% block content %}",
        ),
        Params(
            original="</dj-block 'content'>",
            replacement="{% endblock content %}",
        ),
        Params(
            original="<dj-block content>",
            replacement="{% block content %}",
        ),
        Params(
            original="</dj-block content>",
            replacement="{% endblock content %}",
        ),
    ),
)
def test_typical(original, replacement):
    actual = get_tag_replacements(original, raise_for_missing_start_tag=False)

    for tag_replacement in actual:
        assert tag_replacement.original == original
        assert tag_replacement.replacement == replacement


@pytest.mark.parametrize(
    Params._fields,
    (
        Params(
            original="<dj-include 'partial' />",
            replacement="<dj-partial>{% include 'partial.html' %}</dj-partial>",
        ),
    ),
)
def test_no_extension(original, replacement):
    actual = get_tag_replacements(original, raise_for_missing_start_tag=False)

    for tag_replacement in actual:
        assert tag_replacement.original == original
        assert tag_replacement.replacement == replacement


@pytest.mark.parametrize(
    Params._fields,
    (
        Params(
            original="<$partial />",
            replacement="<dj-partial>{% include 'partial.html' %}</dj-partial>",
        ),
        Params(
            original="<$partial! />",
            replacement=_shadowify("{% include 'partial.html' %}"),
        ),
        Params(
            original="<$partial!>",
            replacement="<dj-partial><template shadowrootmode='open'>{% include 'partial.html' %}",
        ),
        Params(
            original="</$partial!>",
            replacement="</template></dj-partial>",
        ),
        Params(
            original="<$directory/partial />",
            replacement="<dj-directory-partial>{% include 'directory/partial.html' %}</dj-directory-partial>",
        ),
    ),
)
def test_initial_tag_regex(original, replacement, settings):
    settings.ANGLES = {"initial_tag_regex": r"(dj-|\$)"}

    actual = get_tag_replacements(original, raise_for_missing_start_tag=False)

    for tag_replacement in actual:
        assert tag_replacement.original == original
        assert tag_replacement.replacement == replacement


@pytest.mark.parametrize(
    Params._fields,
    (
        Params(
            original="<Partial />",
            replacement="<dj-partial>{% include 'Partial.html' %}</dj-partial>",
        ),
    ),
)
def test_initial_tag_regex_for_react_style(original, replacement, settings):
    settings.ANGLES = {
        "initial_tag_regex": r"(dj-|(?=[A-Z]))",
        "lower_case_tag": False,
        "kebab_case_tag": False,
    }

    actual = get_tag_replacements(original, raise_for_missing_start_tag=False)

    for tag_replacement in actual:
        assert tag_replacement.original == original
        assert tag_replacement.replacement == replacement


@pytest.mark.parametrize(
    Params._fields,
    (
        Params(
            original="<Partial />",
            replacement="<dj-partial>{% include 'partial.html' %}</dj-partial>",
        ),
    ),
)
def test_lower_case_tag(original, replacement, settings):
    settings.ANGLES = {"initial_tag_regex": r"(dj-|(?=[A-Z]))", "lower_case_tag": True}

    actual = get_tag_replacements(original, raise_for_missing_start_tag=False)

    for tag_replacement in actual:
        assert tag_replacement.original == original
        assert tag_replacement.replacement == replacement


@pytest.mark.parametrize(
    Params._fields,
    (
        Params(
            original="<PartialOne />",
            replacement="<dj-partial-one>{% include 'partial-one.html' %}</dj-partial-one>",
        ),
        Params(
            original="<PartialTwo />",
            replacement="<dj-partial-two>{% include 'partial-two.html' %}</dj-partial-two>",
        ),
    ),
)
def test_kebab_case_tag(original, replacement, settings):
    settings.ANGLES = {"initial_tag_regex": r"(?=[A-Z])", "kebab_case_tag": True}

    actual = get_tag_replacements(original, raise_for_missing_start_tag=False)

    for tag_replacement in actual:
        assert tag_replacement.original == original
        assert tag_replacement.replacement == replacement


@pytest.mark.parametrize(
    Params._fields,
    (
        Params(
            original="<blob 'partial.html' />",
            replacement="{% include 'partial.html' %}",
        ),
    ),
)
def test_mappers_string(original, replacement, settings):
    settings.ANGLES = {
        "initial_tag_regex": None,
        "mappers": {
            "blob": "include",
        },
    }
    clear_tag_map()

    actual = get_tag_replacements(original, raise_for_missing_start_tag=False)

    for tag_replacement in actual:
        assert tag_replacement.original == original
        assert tag_replacement.replacement == replacement


@pytest.mark.parametrize(
    Params._fields,
    (
        Params(
            original="<blob />",
            replacement="blob2",
        ),
    ),
)
def test_mappers_callable(original, replacement, settings):
    settings.ANGLES = {
        "initial_tag_regex": None,
        "mappers": {"blob": lambda tag: "blob2"},
    }
    clear_tag_map()

    actual = get_tag_replacements(original, raise_for_missing_start_tag=False)

    for tag_replacement in actual:
        assert tag_replacement.original == original
        assert tag_replacement.replacement == replacement


@pytest.mark.parametrize(
    Params._fields,
    (
        Params(
            original="<dj-image 'img/blob.png' />",
            replacement="<img src=\"{% static 'img/blob.png' %}\" />",
        ),
        Params(
            original="<dj-image 'img/test.jpg' id=\"test\" />",
            replacement='<img src="{% static \'img/test.jpg\' %}" id="test" />',
        ),
    ),
)
def test_image(original, replacement):
    actual = get_tag_replacements(original, raise_for_missing_start_tag=False)

    for tag_replacement in actual:
        assert tag_replacement.original == original
        assert tag_replacement.replacement == replacement


@pytest.mark.parametrize(
    Params._fields,
    (
        Params(
            original="<dj-css 'css/style.css' />",
            replacement='<link href="{% static \'css/style.css\' %}" rel="stylesheet" />',
        ),
    ),
)
def test_css(original, replacement):
    actual = get_tag_replacements(original, raise_for_missing_start_tag=False)

    for tag_replacement in actual:
        assert tag_replacement.original == original
        assert tag_replacement.replacement == replacement


def test_no_prefix(settings):
    settings.ANGLES["initial_tag_regex"] = r"(?=\w)"

    actual = get_tag_replacements("<block name='content'>", raise_for_missing_start_tag=False)

    assert actual[0].original == "<block name='content'>"
    assert actual[0].replacement == "{% block content %}"


def test_no_prefix_with_default_mapper(settings):
    settings.ANGLES["initial_tag_regex"] = r"(?=\w)"

    actual = get_tag_replacements("<partial />", raise_for_missing_start_tag=False)

    assert actual[0].original == "<partial />"
    assert actual[0].replacement == "<dj-partial>{% include 'partial.html' %}</dj-partial>"


def test_no_prefix_without_default_mapper(settings):
    settings.ANGLES["default_mapper"] = None
    settings.ANGLES["initial_tag_regex"] = r"(?=\w)"

    expected = []
    actual = get_tag_replacements("<partial />", raise_for_missing_start_tag=False)

    assert actual == expected


def test_no_prefix_map_explicit_tags_only(settings):
    settings.ANGLES["map_explicit_tags_only"] = True
    settings.ANGLES["initial_tag_regex"] = r"(?=\w)"

    expected = []
    actual = get_tag_replacements("<partial />", raise_for_missing_start_tag=False)

    assert actual == expected
