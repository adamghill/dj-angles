import inspect
import logging

from django.template import Context, Node, TemplateSyntaxError, Variable

from dj_angles.evaluator import ParsedFunction, TemplateVariable, eval_value
from dj_angles.templatetags.template import NodeListRenderer
from dj_angles.tokenizer import yield_tokens

logger = logging.getLogger(__name__)


def get_tag_args(token, tag_name: str, min_args: int = 1) -> tuple[ParsedFunction, list[str], str | None]:
    """
    Parses the token to get the arguments for a tag.

    Args:
        token: The token to parse.
        tag_name: The name of the tag.
        min_args: The minimum number of arguments required.

    Returns:
        tuple[ParsedFunction, list[str], str | None]: The parsed function, the remaining arguments,
            and the context variable name.
    """

    contents = list(yield_tokens(token.contents, " ", handle_quotes=True, handle_parenthesis=True))

    # The first content is always the name of the tag, so pop it off
    contents.pop(0)

    if len(contents) < min_args:
        raise TemplateSyntaxError(f"{tag_name} template tag requires at least {min_args} argument")

    parsed_function = ParsedFunction(contents[0])

    # Collect the rest of the template tag arguments, including context variable if present
    context_variable_name = None
    template_tag_arguments = contents[1:]

    args = []

    for idx, arg in enumerate(template_tag_arguments):
        if arg == "as":
            if len(template_tag_arguments) < idx + 2:
                raise TemplateSyntaxError("Missing variable name after 'as'")
            elif len(template_tag_arguments) > idx + 2:
                raise TemplateSyntaxError("Too many arguments after 'as'")

            context_variable_name = template_tag_arguments[idx + 1]
            break
        else:
            args.append(arg)

    return (parsed_function, args, context_variable_name)


def resolve(context, arg):
    """
    Resolves a template variable based on the context if it's a `TemplateVariable`. Otherwise,
    evaluate the arg.

    Args:
        param context: The template context.
        param arg: The variable to resolve.

    Returns:
        The resolved value of the variable.
    """

    if isinstance(arg, TemplateVariable):
        resolved = Variable(arg.name).resolve(context)

        # If the template variable has portions, resolve them
        if arg.portions:
            for portion in arg.portions:
                if hasattr(resolved, portion.name):
                    resolved = getattr(resolved, portion.name)
                else:
                    raise TemplateSyntaxError(f"{arg.name} does not have attribute {portion.name}")

        return resolved

    return eval_value(arg)


class CallNode(Node):
    def __init__(self, parsed_function, context_variable_name):
        self.parsed_function = parsed_function
        self.context_variable_name = context_variable_name

    def resolve_args(self, context, portion):
        args = portion.args

        if isinstance(args, TemplateVariable):
            args = resolve(context, args)

        if isinstance(args, str):
            # A "string" for args means it's a splat
            args = [resolve(context, args)]
        else:
            resolved_args = []

            for arg in args:
                if isinstance(arg, dict):
                    resolved_args.append(arg)

                    for k, v in list(arg.items()):
                        arg[resolve(context, k)] = resolve(context, v)
                elif isinstance(arg, list):
                    resolved_args.append([resolve(context, a) for a in arg])

            if resolved_args:
                args = resolved_args
            else:
                args = [resolve(context, arg) for arg in args]

        return args

    def resolve_kwargs(self, context, portion):
        kwargs = {}

        for key, value in portion.kwargs.items():
            # `None` key implies that the kwarg is a double splat
            if key is None:
                kwargs = {}

                if isinstance(value, dict):
                    for k, v in list(value.items()):
                        kwargs[resolve(context, k)] = resolve(context, v)
                else:
                    kwargs = resolve(context, value)
            else:
                kwargs[resolve(context, key)] = resolve(context, value)

        return kwargs

    def get_result(self, context, obj, portion):
        args = self.resolve_args(context, portion)
        kwargs = self.resolve_kwargs(context, portion)

        result = None

        if obj is None:
            result = context.get(portion.name)
        elif callable(obj):
            result = obj

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
                obj = obj[portion.name]
            elif hasattr(obj, portion.name):
                obj = getattr(obj, portion.name)

            if callable(obj):
                obj = self.get_result(context, obj, portion)
            elif isinstance(obj, NodeListRenderer):
                renderer = obj

                if len(renderer.parsed_function.portions) > 1:
                    raise TemplateSyntaxError("Invalid template renderer")

                template_context = {}
                template_last_portion = renderer.parsed_function.portions[-1]

                for key, value in template_last_portion.kwargs.items():
                    template_context[key] = resolve(context, value)

                if len(self.parsed_function.portions) > 1:
                    raise TemplateSyntaxError("Invalid template call")

                call_last_portion = self.parsed_function.portions[-1]

                if len(template_last_portion.args) != len(call_last_portion.args):
                    raise TemplateSyntaxError("Invalid number of arguments")

                for arg_idx, arg in enumerate(call_last_portion.args):
                    arg_name = template_last_portion.args[arg_idx].name
                    template_context[arg_name] = resolve(context, arg)

                for key, value in call_last_portion.kwargs.items():
                    template_context[key] = resolve(context, value)

                node_list_context = Context({})

                if renderer.include_context:
                    node_list_context = Context(context.flatten())
                else:
                    node_list_context.template = context.template

                node_list_context.update(template_context)

                return renderer.render(node_list_context)

        if self.context_variable_name is not None:
            context.push({self.context_variable_name: obj})
            return ""

        # Must render a string
        return str(obj)


def do_call(parser, token) -> CallNode:  # noqa: ARG001
    """
    Parses the token to get all the pieces needed to call the function.

    Args:
        parser: The template parser.
        token: The token to parse.

    Returns:
        CallNode: Handles running the function and storing the result in the context.
    """

    """
    Split the contents by whitespace. Examples:
        - "call model.some_function('hello goodbye') as output_variable"
        - "call model.some_function('hello', 2) as output_variable"
        - "call model.some_function(arg1, arg2) as output_variable"
    """

    (parsed_function, _, context_variable_name) = get_tag_args(token, "call")

    return CallNode(parsed_function, context_variable_name)
