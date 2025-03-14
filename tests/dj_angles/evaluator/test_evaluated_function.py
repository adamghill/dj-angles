from dj_angles.evaluator import EvaluatedFunction, eval_function
from dj_angles.templatetags.call import TemplateVariable


def test_no_args():
    expected = EvaluatedFunction("set_name", [], {})
    actual = eval_function("set_name()")

    assert expected == actual


def test_no_parens():
    expected = EvaluatedFunction("set_name", [], {})
    actual = eval_function("set_name")

    assert expected == actual


def test_str_arg():
    expected = EvaluatedFunction("set_name", ["Bob"], {})
    actual = eval_function("set_name('Bob')")

    assert expected == actual


def test_template_variable():
    actual = eval_function("set_name(request)")

    assert actual.function_name == "set_name"
    assert len(actual.args) == 1
    assert isinstance(actual.args[0], TemplateVariable)
    assert actual.args[0].name == "request"
    assert actual.kwargs == {}


def test_int_arg():
    expected = EvaluatedFunction("set_name", [1], {})
    actual = eval_function("set_name(1)")

    assert expected == actual


def test_str_kwarg():
    expected = EvaluatedFunction("set_name", [], {"name": "Bob"})
    actual = eval_function("set_name(name='Bob')")

    assert expected == actual
