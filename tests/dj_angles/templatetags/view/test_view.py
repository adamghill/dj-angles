import pytest
from django.http import HttpResponse
from django.template import Context, Template
from django.test import override_settings
from django.views import View


def simple_view(request):
    return HttpResponse("Simple View")


def view_with_arg(request, arg1):
    return HttpResponse(f"Arg: {arg1}")


def view_with_kwargs(request, arg1=None):
    return HttpResponse(f"Kwarg: {arg1}")


class ClassView(View):
    def get(self, request):  # noqa: ARG002
        return HttpResponse("Class View")


class ClassViewWithArg(View):
    def get(self, request, arg1):  # noqa: ARG002
        return HttpResponse(f"Class Arg: {arg1}")


@pytest.fixture
def context(rf):
    request = rf.get("/")
    return Context({"request": request})


def test_tag_fbv(context):
    template = Template("{% load dj_angles %} {% view 'tests.dj_angles.templatetags.view.test_view.simple_view' %}")
    rendered = template.render(context)
    assert "Simple View" in rendered


def test_tag_fbv_arg(context):
    template = Template(
        "{% load dj_angles %} {% view 'tests.dj_angles.templatetags.view.test_view.view_with_arg' 'Testing' %}"
    )
    rendered = template.render(context)
    assert "Arg: Testing" in rendered


def test_tag_cbv_class(context):
    template = Template("{% load dj_angles %} {% view 'tests.dj_angles.templatetags.view.test_view.ClassView' %}")
    rendered = template.render(context)
    assert "Class View" in rendered


def test_tag_cbv_as_view(context):
    template = Template(
        "{% load dj_angles %} {% view 'tests.dj_angles.templatetags.view.test_view.ClassView.as_view' %}"
    )
    rendered = template.render(context)
    assert "Class View" in rendered


def test_tag_cbv_arg(context):
    template = Template(
        "{% load dj_angles %} {% view 'tests.dj_angles.templatetags.view.test_view.ClassViewWithArg' 'Params' %}"
    )
    rendered = template.render(context)
    assert "Class Arg: Params" in rendered


def test_missing_view(context):
    template = Template("{% load dj_angles %} {% view 'tests.dj_angles.templatetags.view.test_view.Missing' %}")
    with pytest.raises(ImportError):
        template.render(context)


@override_settings(ROOT_URLCONF="tests.dj_angles.templatetags.view.test_urls")
@pytest.mark.urls("tests.dj_angles.templatetags.view.test_urls")
def test_named_view(context):
    template = Template("{% load dj_angles %} {% view 'named_view' %}")
    rendered = template.render(context)
    assert "Named View" in rendered


@override_settings(ROOT_URLCONF="tests.dj_angles.templatetags.view.test_urls")
@pytest.mark.urls("tests.dj_angles.templatetags.view.test_urls")
def test_named_view_arg(context):
    template = Template("{% load dj_angles %} {% view 'named_view_args' 'FoundIt' %}")
    rendered = template.render(context)
    assert "Named View Arg: FoundIt" in rendered
