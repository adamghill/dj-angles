import pytest
from django.template import Context, Template
from django.template.exceptions import TemplateSyntaxError


def test_template_missing_args():
    template_string = "{% load dj_angles %}{% template %}{% endtemplate %}"
    with pytest.raises(TemplateSyntaxError, match="template requires at least 1 argument"):
        Template(template_string)


def test_template_invalid_renderer():
    # Assuming foo.bar triggers > 1 portions
    template_string = "{% load dj_angles %}{% template foo.bar %}{% endtemplate %}"
    with pytest.raises(TemplateSyntaxError, match="Invalid template renderer"):
        t = Template(template_string)
        t.render(Context({}))
