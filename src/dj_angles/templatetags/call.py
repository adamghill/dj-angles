import inspect
import logging

from django.template import Node, TemplateSyntaxError, Variable
from django.template.base import VariableDoesNotExist

from dj_angles.evaluator import ParsedFunction, eval_value
from dj_angles.tokenizer import yield_tokens

logger = logging.getLogger(__name__)


def resolve(context, arg):
    """
    Resolves a template variable based on the context.

    Args:
        param context: The template context.
        param arg: The variable to resolve.

    Returns:
        The resolved value of the variable.
    """

    if arg in context:
        try:
            return Variable(arg).resolve(context)
        except VariableDoesNotExist:
            pass

    return eval_value(arg)


class CallNode(Node):
    def __init__(self, parsed_function, context_variable_name):
        self.parsed_function = parsed_function
        self.context_variable_name = context_variable_name

    def resolve_args(self, context, portion):
        if isinstance(portion.args, str):
            # A "string" for args means it's a splat
            args = resolve(context, portion.args)
        else:
            args = [resolve(context, arg) for arg in portion.args]

        return args

    def resolve_kwargs(self, context, portion):
        kwargs = {}

        for key, value in portion.kwargs.items():
            if key is None:
                # `None` key implies that the kwarg is a double splat
                try:
                    kwargs.update(resolve(context, value))
                except TypeError:
                    kwargs.update(value)
            else:
                kwargs[resolve(context, key)] = resolve(context, value)

        return kwargs

    def get_result(self, context, obj, portion):
        args = self.resolve_args(context, portion)
        kwargs = self.resolve_kwargs(context, portion)

        result = None

        if obj is None:
            result = context[portion.name]
        elif hasattr(obj, portion.name):
            result = getattr(obj, portion.name)
        elif callable(obj):
            result = obj
        elif portion.name in context:
            result = resolve(context, portion.name)

        if inspect.ismethod(result) or inspect.isfunction(result):
            result = result(*args, **kwargs)

        return result

    def render(self, context):
        """Execute the function with the provided arguments and stores the results in context."""

        obj = None

        for idx, portion in enumerate(self.parsed_function.portions):
            if idx == 0:
                obj = self.get_result(context, obj, portion)
            elif isinstance(obj, dict):
                # TODO: make test for this
                obj = obj[portion.name]
            elif hasattr(obj, portion.name):
                obj = getattr(obj, portion.name)

            if callable(obj):
                obj = self.get_result(context, obj, portion)

        if self.context_variable_name is not None:
            context[self.context_variable_name] = obj

        # Must render a string
        return ""


def do_call(parser, token) -> CallNode:  # noqa: ARG001
    """Parses the token to get all the pieces needed to call the function.

    Args:
        parser: The template parser.
        token: The token to parse.

    Returns:
        CallNode: Handles running the function and storing the result in the context.
    """

    """
    Split the contents by whitespace. Examples:
        - "execute model.some_function arg1 as output_variable"
        - "execute model.some_function 'hello goodbye' as output_variable"
        - "execute model.some_function(arg1, arg2) as output_variable"
    """
    contents = list(yield_tokens(token.contents, " ", handle_quotes=True, handle_parenthesis=True))

    # The first content is always the name of the tag, so pop it off
    contents.pop(0)

    if len(contents) < 1:
        raise TemplateSyntaxError("call template tag requires at least 1 argument")

    parsed_function = ParsedFunction(contents[0])

    # Collect the rest of the template tag arguments, including context variable if present
    context_variable_name = None
    template_tag_arguments = contents[1:]

    for idx, arg in enumerate(template_tag_arguments):
        if arg == "as":
            if len(template_tag_arguments) < idx + 2:
                raise TemplateSyntaxError("Missing variable name after 'as'")
            elif len(template_tag_arguments) > idx + 2:
                raise TemplateSyntaxError("Too many arguments after 'as'")

            context_variable_name = template_tag_arguments[idx + 1]
            break

        # Handle arguments that are not handled by parsing the contents with `ParsedFunction`
        # i.e. arguments that are not inside parenthesis
        parsed_function.portions[-1].args.append(arg)

    return CallNode(parsed_function, context_variable_name)
