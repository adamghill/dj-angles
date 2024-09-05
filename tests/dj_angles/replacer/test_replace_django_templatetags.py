from dj_angles.replacer import replace_django_templatetags


def test_typical():
    expected = """{% extends 'base.html' %}

{% block content %}
  <input />

  {% include 'partial.html' %}

  {% include 'another-directory/another-partial.html' %}

  {% debug %}
{% endblock content %}"""

    actual = replace_django_templatetags("""<dj-extends 'base.html' />

<dj-block content>
  <input />

  <dj-partial />

  <dj-another-directory/another-partial />

  <dj-debug />
</dj-block content>""")

    assert actual == expected


def test_extends():
    expected = "{% extends 'base.html' %}"
    actual = replace_django_templatetags("<dj-extends 'base.html' />")

    assert actual == expected
