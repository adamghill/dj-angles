import ast
import logging
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from functools import lru_cache
from uuid import UUID

from django.utils.dateparse import (
    parse_date,
    parse_datetime,
    parse_duration,
    parse_time,
)

from dj_angles.tokenizer import yield_tokens

logger = logging.getLogger(__name__)


CASTERS = {
    datetime: parse_datetime,
    time: parse_time,
    date: parse_date,
    timedelta: parse_duration,
    UUID: UUID,
}


@dataclass
class EvaluatedFunction:
    function_name: str
    args: list = field(default_factory=list)
    kwargs: dict = field(default_factory=dict)

    def __iter__(self):
        yield self.function_name
        yield self.args
        yield self.kwargs


@dataclass
class Portion:
    name: str
    args: list = field(default_factory=list)
    kwargs: dict = field(default_factory=dict)

    def __init__(self, name: str):
        self.args = []
        self.kwargs = {}
        self.name = name

        if self.name.endswith("()"):
            self.name = self.name[:-2]
        elif "(" in self.name and ")" in self.name:
            (self.name, self.args, self.kwargs) = eval_function(self.name)


@dataclass
class ParsedFunction:
    function_name: str
    portions: list[Portion] = field(default_factory=list)

    def __init__(self, function_name: str):
        self.function_name = function_name
        self.portions = []

        self.parse_function()

    def parse_function(self):
        for token in yield_tokens(self.function_name, ".", handle_quotes=True, handle_parenthesis=True):
            portion = Portion(token)

            self.portions.append(portion)


def cast_value(value):
    """Try to cast a value."""

    for caster in CASTERS.values():
        try:
            casted_value = caster(value)

            if casted_value:
                value = casted_value
                break
        except ValueError:
            pass

    return value


def eval_value(value):
    """
    Uses `ast.literal_eval` to parse strings into an appropriate Python primitive.

    Also returns an appropriate object for strings that look like they represent datetime,
    date, time, duration, or UUID.
    """

    if isinstance(value, ast.Starred):
        value = value.value

    try:
        value = ast.literal_eval(value)
    except SyntaxError:
        value = cast_value(value)
    except ValueError:
        # Handle Name node that represents a template variable since it does not "look" like a string that AST
        # understands; this will get resolved when rendering the CallNode later
        if isinstance(value, ast.Name):
            value = value.id

    return value


@lru_cache(maxsize=128, typed=True)
def eval_function(function_string: str) -> EvaluatedFunction:
    """
    Parses the method name from a string into a set of parameters to pass to a method.

    Args:
        param function_string: String representation of a method name with parameters,
            e.g. "set_name('Bob')"

    Returns:
        Tuple of method_name, a list of arguments and a dict of keyword arguments.
    """

    args: list = []
    kwargs: dict = {}

    function_name = function_string.strip()
    tree = ast.parse(function_name, "eval")
    statement = tree.body[0].value  # type: ignore

    if tree.body and isinstance(statement, ast.Call):
        call = tree.body[0].value  # type: ignore
        function_name = call.func.id

        if call.args and call.args[0] and isinstance(call.args[0], ast.Starred):
            args = eval_value(call.args[0])
        else:
            args = [eval_value(arg) for arg in call.args]

        kwargs = {kw.arg: eval_value(kw.value) for kw in call.keywords}

    return EvaluatedFunction(function_name, args, kwargs)
