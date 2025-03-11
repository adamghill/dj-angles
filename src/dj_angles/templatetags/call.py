import logging

from django.template import Node, TemplateSyntaxError, Variable
from django.template.base import VariableDoesNotExist

from dj_angles.evaluator import ParsedFunction, eval_value
from dj_angles.tokenizer import yield_tokens

logger = logging.getLogger(__name__)

# <dj-call function="quip.has_vote" request="request" as="has_vote" />


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

    def _get_function_from_context(self, context):
        fn = None

        if self.parsed_function.object_name:
            obj = None

            # Handle nested objects
            if self.parsed_function.object_tokens:
                for idx, token in enumerate(self.parsed_function.object_tokens):
                    if idx == 0:
                        obj = context[token]
                    elif isinstance(obj, dict):
                        obj = obj[token]
                    else:
                        obj = getattr(obj, token)
            else:
                obj = context[self.parsed_function.object_name]

            fn = getattr(obj, self.parsed_function.function_name)
            fn = getattr(obj, self.parsed_function.function_name)
        else:
            fn = context.get(self.parsed_function.function_name)

        return fn

    def render(self, context):
        """Execute the function with the provided arguments and stores the results in context."""

        fn = self._get_function_from_context(context)

        if fn is None:
            raise TemplateSyntaxError(f"Function '{self.parsed_function.function_name}' not found")

        if isinstance(self.parsed_function.args, str):
            # A "string" for args means it's a splat
            args = resolve(context, self.parsed_function.args)
        else:
            args = [resolve(context, arg) for arg in self.parsed_function.args]

        kwargs = {}

        for key, value in self.parsed_function.kwargs.items():
            if key is None:
                # `None` key implies that the kwarg is a double splat
                try:
                    kwargs.update(resolve(context, value))
                except TypeError:
                    kwargs.update(value)
            else:
                kwargs[resolve(context, key)] = resolve(context, value)

        result = None

        if callable(fn):
            result = fn(*args, **kwargs)
        else:
            result = fn

        if self.context_variable_name is not None:
            context[self.context_variable_name] = result

        # Must return an empty string
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

        parsed_function.args.append(arg)

    return CallNode(parsed_function, context_variable_name)
