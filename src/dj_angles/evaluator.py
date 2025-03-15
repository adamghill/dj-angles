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


@dataclass
class Caster:
    CASTERS = {  # noqa: RUF012
        datetime: parse_datetime,
        time: parse_time,
        date: parse_date,
        timedelta: parse_duration,
        UUID: UUID,
    }

    def __init__(self, value):
        self.value = value

    def cast(self):
        """Try to cast a value."""

        for caster in self.CASTERS.values():
            try:
                casted_value = caster(self.value)

                if casted_value is not None:
                    return casted_value
            except (ValueError, TypeError, AttributeError):
                pass

        return self.value


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


@dataclass
class TemplateVariable:
    name: str
    portions: list[Portion] = field(default_factory=list)

    def __init__(self, name: ast.Name):
        self._name = name
        self.name = name.id
        self.portions = []

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, TemplateVariable):
            return self.name == other.name

        return False


def eval_value(value):
    """
    Uses `ast.literal_eval` to parse strings into an appropriate Python primitive.

    Also returns an appropriate object for strings that look like they represent datetime,
    date, time, duration, or UUID.
    """

    # Handle AST name, attribute, or call first
    if isinstance(value, ast.Name):
        return TemplateVariable(value)
    elif isinstance(value, ast.Attribute):
        resolved = eval_value(value.value)

        if isinstance(resolved, TemplateVariable):
            resolved.portions.append(Portion(value.attr))

        return resolved
    elif isinstance(value, ast.Call):
        resolved = eval_value(value.func)

        # If it was an attribute, it should have been added to portions already,
        # but we need to add args and kwargs to it (which we can find because
        # it's the last portion)
        if isinstance(value.func, ast.Attribute):
            resolved.portions[-1].args = [eval_value(arg) for arg in value.args]
            resolved.portions[-1].kwargs = {kw.arg: eval_value(kw.value) for kw in value.keywords}

        return resolved

    # Handle starred, dictionaries, and lists
    if isinstance(value, ast.Starred):
        value = eval_value(value.value)
    elif isinstance(value, ast.Dict):
        data = {}

        for idx, key in enumerate(value.keys):
            data[eval_value(key)] = eval_value(value.values[idx])

        value = data
    elif isinstance(value, ast.List):
        value = [eval_value(v) for v in value.elts]

    # Parse and cast any values
    try:
        value = ast.literal_eval(value)
    except SyntaxError:
        value = Caster(value).cast()
    except ValueError:
        # Ignore ValueError
        pass

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
