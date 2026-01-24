from typing import Optional
from unittest.mock import patch

import pytest
from django.template import TemplateDoesNotExist, TemplateSyntaxError

from dj_angles.replacers.tags import replace_tags as replace_django_template_tags


def _get_template_syntax_error_exception(
    name: str = "name", during: str = "during", message: str = "Fake exception"
) -> Exception:
    exception = TemplateSyntaxError()
    exception.template_debug = {"name": name, "during": during, "message": message}

    return exception


def _get_template_does_not_exist_exception(
    name: str = "index.html",
    during: str = "during",
    message: str = "missing.html",
    tried: list[str] | None = None,
) -> Exception:
    exception = TemplateDoesNotExist(msg="")
    exception.template_debug = {"name": name, "during": during, "message": message}

    if tried is None:
        tried = []

    exception.tried = tried

    return exception


class TestErrorBoundary:
    @patch("dj_angles.replacers.tags._validate_template")
    def test_missing(self, _validate_template):
        _validate_template.side_effect = _get_template_does_not_exist_exception()

        expected = """
<dj-error-boundary>
    <div><template shadowrootmode="open"><div style='border: 1px red solid; padding: 0 24px 0 24px;' class=''><h2>
  index.html
</h2>
<p>
  <em>Could not find the template: 'missing.html'.</em>
</p>
<p>
  <pre><code>{% verbatim %}during{% endverbatim %}</code></pre>
</p>
</div></template></div>
</dj-error-boundary>
    """

        template = """
<dj-error-boundary>
    <dj-include src="missing.html" />
</dj-error-boundary>
    """

        actual = replace_django_template_tags(template)

        assert actual == expected

    @patch("dj_angles.replacers.tags._validate_template")
    def test_missing_multiple(self, _validate_template, settings):
        _validate_template.side_effect = _get_template_does_not_exist_exception(
            name="missing1.html", message="missing1.html"
        )

        settings.DEBUG = True
        expected = """
<dj-error-boundary>
    <div><template shadowrootmode="open"><div style='border: 1px red solid; padding: 0 24px 0 24px;' class=''><h2>
  missing1.html
</h2>
<p>
  <em>Could not find the template: 'missing1.html'.</em>
</p>
<p>
  <pre><code>{% verbatim %}during{% endverbatim %}</code></pre>
</p>
</div></template></div>
</dj-error-boundary>
    """

        template = """
<dj-error-boundary>
    <dj-include src="missing1.html" />
    <dj-include src="missing2.html" />
</dj-error-boundary>
    """

        actual = replace_django_template_tags(template)
        print(actual)

        assert actual == expected

    @patch("dj_angles.replacers.tags._validate_template")
    def test_missing_multiple_same(self, _validate_template, settings):
        _validate_template.side_effect = _get_template_does_not_exist_exception(
            name="missing.html", message="missing.html"
        )

        settings.DEBUG = True
        expected = """
<dj-error-boundary>
    <div><template shadowrootmode="open"><div style='border: 1px red solid; padding: 0 24px 0 24px;' class=''><h2>
  missing.html
</h2>
<p>
  <em>Could not find the template: 'missing.html'.</em>
</p>
<p>
  <pre><code>{% verbatim %}during{% endverbatim %}</code></pre>
</p>
</div></template></div>
</dj-error-boundary>
    """

        template = """
<dj-error-boundary>
    <dj-include src="missing.html" />
    <dj-include src="missing.html" />
</dj-error-boundary>
    """

        actual = replace_django_template_tags(template)

        assert actual == expected

    def test_invalid(self):
        expected = """
<dj-error-boundary>
    <div><template shadowrootmode="open"><div style='border: 1px red solid; padding: 0 24px 0 24px;' class=''><em>Could not parse the remainder: ' variable' from 'invalid variable'</em></div></template></div>
</dj-error-boundary>
        """

        template = """
<dj-error-boundary>
    <dj-include src="invalid_variable.html" />
</dj-error-boundary>
        """

        actual = replace_django_template_tags(template)
        print(actual)

        assert actual == expected


class TestBlockBoundary:
    def test_invalid_no_boundary(self):
        #         expected = """
        # {% block content %}
        #     {% include 'invalid.html' %}
        # {% endblock content %}
        #     """

        template = """
<dj-block name='content'>
    <dj-include src="invalid_variable.html" />
</dj-block>
    """

        with pytest.raises(TemplateSyntaxError):
            replace_django_template_tags(template)

    def test_invalid(self):
        expected = """
{% block content %}
    <div><template shadowrootmode="open"><div style='border: 1px red solid; padding: 0 24px 0 24px;' class=''><em>Could not parse the remainder: ' variable' from 'invalid variable'</em></div></template></div>
{% endblock content %}
    """

        template = """
<dj-block name='content' error-boundary>
    <dj-include src="invalid_variable.html" />
</dj-block>
    """

        actual = replace_django_template_tags(template)
        print(actual)

        assert actual == expected


def test_invalid_no_boundary():
    #         expected = """
    # {% block content %}
    #     {% include 'invalid.html' %}
    # {% endblock content %}
    #     """

    template = """
<dj-block name='content'>
    <dj-include src="invalid_variable.html" />
</dj-block>
    """

    with pytest.raises(TemplateSyntaxError):
        replace_django_template_tags(template)


def test_two_error_boundaries():
    """This shouldn't fail, but it currently does so this documents that fact"""

    template = """
<dj-block name='content' error-boundary>
  <dj-error-boundary>
    <dj-include src="invalid.html" />
  </dj-error-boundary>
</dj-block>
"""

    # with pytest.raises(TemplateDoesNotExist):
    from django.template import Origin

    origin = Origin("test.html")
    a = replace_django_template_tags(template, origin=origin)
