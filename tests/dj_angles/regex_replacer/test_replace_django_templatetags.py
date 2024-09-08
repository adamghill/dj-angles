import pytest

from dj_angles.exceptions import InvalidEndTagError
from dj_angles.regex_replacer import replace_django_template_tags


def test_typical():
    expected = """{% extends 'base.html' %}

{% block content %}
  <input />

  <dj-partial>{% include 'partial.html' %}</dj-partial>

  <dj-another-directory-another-partial>{% include 'another-directory/another-partial.html' %}</dj-another-directory-another-partial>

  {% debug %}
{% endblock content %}"""  # noqa: E501

    actual = replace_django_template_tags("""<dj-extends 'base.html' />

<dj-block content>
  <input />

  <dj-partial />

  <dj-another-directory/another-partial />

  <dj-debug />
</dj-block content>""")

    assert actual == expected


def test_invalid_tag():
    with pytest.raises(InvalidEndTagError) as e:
        replace_django_template_tags("""
<dj-block content>
<input>

<dj-partial>
</dj-block content>""")

    assert e.exconly() == "dj_angles.exceptions.InvalidEndTagError"
    assert e.value.tag.component_name == "block"
    assert e.value.last_tag.component_name == "partial"


def test_extends():
    expected = "{% extends 'base.html' %}"
    actual = replace_django_template_tags("<dj-extends 'base.html' />")

    assert actual == expected
