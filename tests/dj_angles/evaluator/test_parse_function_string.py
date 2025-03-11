from dj_angles.evaluator import EvaluatedFunction, eval_function


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


def test_unknown_arg():
    expected = EvaluatedFunction("set_name", ["request"], {})
    actual = eval_function("set_name(request)")

    assert expected == actual


def test_int_arg():
    expected = EvaluatedFunction("set_name", [1], {})
    actual = eval_function("set_name(1)")

    assert expected == actual


def test_str_kwarg():
    expected = EvaluatedFunction("set_name", [], {"name": "Bob"})
    actual = eval_function("set_name(name='Bob')")

    assert expected == actual
