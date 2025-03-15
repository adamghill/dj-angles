import pytest
from django.template.base import TemplateSyntaxError, Token, TokenType

from dj_angles.evaluator import TemplateVariable
from dj_angles.templatetags.call import do_call


def test_function_name():
    token = Token(TokenType.BLOCK, contents="call set_name as name")
    actual = do_call(None, token)

    assert actual.parsed_function.portions[0].name == "set_name"
    assert actual.parsed_function.portions[0].args == []
    assert actual.parsed_function.portions[0].kwargs == {}
    assert actual.context_variable_name == "name"


def test_no_args():
    token = Token(TokenType.BLOCK, contents="call")

    with pytest.raises(TemplateSyntaxError) as e:
        do_call(None, token)

    assert (
        e.exconly() == "django.template.exceptions.TemplateSyntaxError: call template tag requires at least 1 argument"
    )


def test_no_as():
    token = Token(TokenType.BLOCK, contents="call set_name")
    actual = do_call(None, token)

    assert actual.parsed_function.portions[0].name == "set_name"
    assert actual.parsed_function.portions[0].args == []
    assert actual.parsed_function.portions[0].kwargs == {}
    assert actual.context_variable_name is None


def test_no_context_variable():
    token = Token(TokenType.BLOCK, contents="call set_name as")

    with pytest.raises(TemplateSyntaxError) as e:
        do_call(None, token)

    assert e.exconly() == "django.template.exceptions.TemplateSyntaxError: Missing variable name after 'as'"


def test_multiple_context_variables():
    token = Token(TokenType.BLOCK, contents="call set_name as name another")

    with pytest.raises(TemplateSyntaxError) as e:
        do_call(None, token)

    assert e.exconly() == "django.template.exceptions.TemplateSyntaxError: Too many arguments after 'as'"


def test_str_arg():
    token = Token(TokenType.BLOCK, contents="call set_name('Hello') as name")
    actual = do_call(None, token)

    assert actual.parsed_function.portions[0].name == "set_name"
    assert actual.parsed_function.portions[0].args == ["Hello"]
    assert actual.parsed_function.portions[0].kwargs == {}
    assert actual.context_variable_name == "name"


def test_multiple_args():
    token = Token(TokenType.BLOCK, contents="call set_name('Hello', 8) as name")
    actual = do_call(None, token)

    assert actual.parsed_function.portions[0].name == "set_name"
    assert actual.parsed_function.portions[0].args == ["Hello", 8]
    assert actual.parsed_function.portions[0].kwargs == {}
    assert actual.context_variable_name == "name"


def test_template_variable():
    token = Token(TokenType.BLOCK, contents="call set_name(hello, 8) as name")
    actual = do_call(None, token)

    portion = actual.parsed_function.portions[0]

    assert portion.name == "set_name"
    assert isinstance(portion.args[0], TemplateVariable)
    assert portion.args[0].name == "hello"
    assert portion.args[1] == 8
    assert portion.kwargs == {}
    assert actual.context_variable_name == "name"
