from collections import namedtuple

import pytest

from dj_angles.regex_replacer import clear_tag_map, get_replacements

# Structure to store parameterize data
Params = namedtuple(
    "Params",
    ("template_string", "replacement_string"),
)


def _shadowify(s: str) -> str:
    return f"<dj-partial><template shadowrootmode='open'>{s}</template></dj-partial>"


@pytest.mark.parametrize(
    Params._fields,
    (
        Params(
            template_string="<dj-extends 'base.html' />",
            replacement_string="{% extends 'base.html' %}",
        ),
        Params(
            template_string="<dj-extends parent='base.html' />",
            replacement_string="{% extends 'base.html' %}",
        ),
        Params(
            template_string="<dj-include 'partial.html' />",
            replacement_string="<dj-partial>{% include 'partial.html' %}</dj-partial>",
        ),
        Params(
            template_string="<dj-include 'partial.html' shadow />",
            replacement_string=_shadowify("{% include 'partial.html' %}"),
        ),
        Params(
            template_string="<dj-include 'partial.html' test='hello' />",
            replacement_string="<dj-partial>{% include 'partial.html' test='hello' %}</dj-partial>",
        ),
        Params(
            template_string="<dj-include 'shadow-partial.html' />",
            replacement_string="<dj-shadow-partial>{% include 'shadow-partial.html' %}</dj-shadow-partial>",
        ),
        Params(
            template_string="<dj-partial />",
            replacement_string="<dj-partial>{% include 'partial.html' %}</dj-partial>",
        ),
        Params(
            template_string="<dj-partial test='hello' />",
            replacement_string="<dj-partial>{% include 'partial.html' test='hello' %}</dj-partial>",
        ),
        Params(
            template_string="<dj-shadow-partial />",
            replacement_string="<dj-shadow-partial>{% include 'shadow-partial.html' %}</dj-shadow-partial>",
        ),
        Params(
            template_string="<dj-comment>",
            replacement_string="{% comment %}",
        ),
        Params(
            template_string="</dj-comment>",
            replacement_string="{% endcomment %}",
        ),
        Params(
            template_string="<dj-#>",
            replacement_string="{% comment %}",
        ),
        Params(
            template_string="</dj-#>",
            replacement_string="{% endcomment %}",
        ),
        Params(
            template_string="<dj-verbatim>",
            replacement_string="{% verbatim %}",
        ),
        Params(
            template_string="</dj-verbatim>",
            replacement_string="{% endverbatim %}",
        ),
        Params(
            template_string="<dj-autoescape-on>",
            replacement_string="{% autoescape on %}",
        ),
        Params(
            template_string="</dj-autoescape-on>",
            replacement_string="{% endautoescape %}",
        ),
        Params(
            template_string="</dj-autoescape-off>",
            replacement_string="{% endautoescape %}",
        ),
        Params(
            template_string="<dj-csrf />",
            replacement_string="{% csrf_token %}",
        ),
        Params(
            template_string="<dj-csrf-input />",
            replacement_string="{% csrf_token %}",
        ),
        Params(
            template_string="<dj-block name='content'>",
            replacement_string="{% block content %}",
        ),
        Params(
            template_string="</dj-block name='content'>",
            replacement_string="{% endblock content %}",
        ),
        Params(
            template_string="<dj-block 'content'>",
            replacement_string="{% block content %}",
        ),
        Params(
            template_string="</dj-block 'content'>",
            replacement_string="{% endblock content %}",
        ),
        Params(
            template_string="<dj-block content>",
            replacement_string="{% block content %}",
        ),
        Params(
            template_string="</dj-block content>",
            replacement_string="{% endblock content %}",
        ),
    ),
)
def test_typical(template_string, replacement_string):
    expected = [
        (template_string, replacement_string),
    ]
    actual = get_replacements(template_string, raise_for_missing_start_tag=False)

    assert actual == expected


@pytest.mark.parametrize(
    Params._fields,
    (
        Params(
            template_string="<dj-include 'partial' />",
            replacement_string="<dj-partial>{% include 'partial.html' %}</dj-partial>",
        ),
    ),
)
def test_no_extension(template_string, replacement_string):
    expected = [
        (template_string, replacement_string),
    ]
    actual = get_replacements(template_string, raise_for_missing_start_tag=False)

    assert actual == expected


@pytest.mark.parametrize(
    Params._fields,
    (
        Params(
            template_string="<$partial />",
            replacement_string="<dj-partial>{% include 'partial.html' %}</dj-partial>",
        ),
        Params(
            template_string="<$partial! />",
            replacement_string=_shadowify("{% include 'partial.html' %}"),
        ),
        Params(
            template_string="<$partial!>",
            replacement_string="<dj-partial><template shadowrootmode='open'>{% include 'partial.html' %}",
        ),
        Params(
            template_string="</$partial!>",
            replacement_string="</template></dj-partial>",
        ),
        Params(
            template_string="<$directory/partial />",
            replacement_string="<dj-directory-partial>{% include 'directory/partial.html' %}</dj-directory-partial>",
        ),
    ),
)
def test_initial_tag_regex(template_string, replacement_string, settings):
    settings.ANGLES = {"initial_tag_regex": r"(dj-|\$)"}

    expected = [
        (template_string, replacement_string),
    ]
    actual = get_replacements(template_string, raise_for_missing_start_tag=False)

    assert actual == expected


@pytest.mark.parametrize(
    Params._fields,
    (
        Params(
            template_string="<Partial />",
            replacement_string="<dj-partial>{% include 'Partial.html' %}</dj-partial>",
        ),
    ),
)
def test_initial_tag_regex_for_react_style(template_string, replacement_string, settings):
    settings.ANGLES = {
        "initial_tag_regex": r"(dj-|(?=[A-Z]))",
        "lower_case_tag": False,
        "slugify_tag": False,
    }

    expected = [
        (template_string, replacement_string),
    ]
    actual = get_replacements(template_string, raise_for_missing_start_tag=False)

    assert actual == expected


@pytest.mark.parametrize(
    Params._fields,
    (
        Params(
            template_string="<Partial />",
            replacement_string="<dj-partial>{% include 'partial.html' %}</dj-partial>",
        ),
    ),
)
def test_lower_case_tag(template_string, replacement_string, settings):
    settings.ANGLES = {"initial_tag_regex": r"(dj-|(?=[A-Z]))", "lower_case_tag": True}

    expected = [
        (template_string, replacement_string),
    ]
    actual = get_replacements(template_string, raise_for_missing_start_tag=False)

    assert actual == expected


@pytest.mark.parametrize(
    Params._fields,
    (
        Params(
            template_string="<PartialOne />",
            replacement_string="<dj-partial-one>{% include 'partial-one.html' %}</dj-partial-one>",
        ),
        Params(
            template_string="<PartialTwo />",
            replacement_string="<dj-partial-two>{% include 'partial-two.html' %}</dj-partial-two>",
        ),
    ),
)
def test_slugify_tag(template_string, replacement_string, settings):
    settings.ANGLES = {"initial_tag_regex": r"(?=[A-Z])", "slugify_tag": True}

    expected = [
        (template_string, replacement_string),
    ]
    actual = get_replacements(template_string, raise_for_missing_start_tag=False)

    assert actual == expected


@pytest.mark.parametrize(
    Params._fields,
    (
        Params(
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
    clear_tag_map()

    expected = [
        (template_string, replacement_string),
    ]
    actual = get_replacements(template_string, raise_for_missing_start_tag=False)

    assert actual == expected


@pytest.mark.parametrize(
    Params._fields,
    (
        Params(
            template_string="<blob />",
            replacement_string="blob2",
        ),
    ),
)
def test_mappers_callable(template_string, replacement_string, settings):
    settings.ANGLES = {
        "initial_tag_regex": None,
        "mappers": {"blob": lambda tag: "blob2"},  # noqa: ARG005
    }
    clear_tag_map()

    expected = [
        (template_string, replacement_string),
    ]
    actual = get_replacements(template_string, raise_for_missing_start_tag=False)

    assert actual == expected


@pytest.mark.parametrize(
    Params._fields,
    (
        Params(
            template_string="<dj-image 'img/blob.png' />",
            replacement_string="<img src=\"{% static 'img/blob.png' %}\" />",
        ),
        Params(
            template_string="<dj-image 'img/test.jpg' id=\"test\" />",
            replacement_string='<img src="{% static \'img/test.jpg\' %}" id="test" />',
        ),
    ),
)
def test_image(template_string, replacement_string):
    expected = [
        (template_string, replacement_string),
    ]
    actual = get_replacements(template_string, raise_for_missing_start_tag=False)

    assert actual == expected


@pytest.mark.parametrize(
    Params._fields,
    (
        Params(
            template_string="<dj-css 'css/style.css' />",
            replacement_string='<link href="{% static \'css/style.css\' %}" rel="stylesheet" />',
        ),
    ),
)
def test_css(template_string, replacement_string):
    expected = [
        (template_string, replacement_string),
    ]
    actual = get_replacements(template_string, raise_for_missing_start_tag=False)

    assert actual == expected
