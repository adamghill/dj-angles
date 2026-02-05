import ast
import inspect
import logging

from django.template import TemplateSyntaxError
from django.urls import NoReverseMatch, resolve, reverse
from django.utils.module_loading import import_string
from django.views import View

from dj_angles.evaluator import eval_value
from dj_angles.templatetags.call import CallNode, get_tag_args

logger = logging.getLogger(__name__)


class ViewNode(CallNode):
    def render(self, context):
        if "request" not in context:
            return ""

        path_parts = []
        args = []
        kwargs = {}

        for portion in self.parsed_function.portions:
            path_parts.append(portion.name)

            p_args = self.resolve_args(context, portion)
            p_kwargs = self.resolve_kwargs(context, portion)

            args.extend(p_args)
            kwargs.update(p_kwargs)

        full_path = ".".join(path_parts)
        full_path = full_path.replace("'", "").replace('"', "")

        # Try to reverse the name to find the view
        # We use strict arguments matching for reverse
        resolved_view = None
        resolved_args = []
        resolved_kwargs = {}

        try:
            # If kwargs are provided, reverse prefers them over args usually,
            # but we pass what we have.
            url = reverse(full_path, args=args, kwargs=kwargs)
            match = resolve(url)
            resolved_view = match.func
            resolved_args = match.args
            resolved_kwargs = match.kwargs
        except NoReverseMatch:
            # Fallback to import_string
            pass

        if resolved_view:
            view_func = resolved_view
            # We use the args/kwargs from the RESOLVED url, not the ones passed to the tag,
            # because the tag args were consumed to make the URL.
            args = resolved_args
            kwargs = resolved_kwargs
        else:
            try:
                obj = import_string(full_path)
            except ImportError:
                if "." in full_path:
                    try:
                        parent, method = full_path.rsplit(".", 1)
                        parent_obj = import_string(parent)
                        obj = getattr(parent_obj, method)
                    except (ImportError, AttributeError) as e:
                        raise ImportError(f"Could not import {full_path}") from e
                else:
                    raise
            view_func = obj

            # Handle class-based views for imported objects
            if isinstance(obj, type) and issubclass(obj, View):
                view_func = obj.as_view()
            elif callable(obj) and getattr(obj, "__name__", "") == "as_view" and inspect.ismethod(obj):
                view_func = obj()

        response = view_func(context["request"], *args, **kwargs)

        if hasattr(response, "render"):
            response.render()

        content = response.content.decode("utf-8")

        # Store rendered content in the context if a variable name was specified
        if self.context_variable_name:
            context.push({self.context_variable_name: content})
            return ""

        return content


def do_view(parser, token) -> ViewNode:  # noqa: ARG001
    """
    Parses the token to get all the pieces needed to call the view.

    Args:
        parser: The template parser.
        token: The token to parse.

    Returns:
        ViewNode: The view node.
    """

    (parsed_function, args, context_variable_name) = get_tag_args(token, "view")

    extra_args = []

    for arg in args:
        # Parse the argument (literals, variables, etc)
        try:
            tree = ast.parse(arg, mode="eval")

            # eval_value handles AST nodes and converts names to TemplateVariable
            value = eval_value(tree.body)
            extra_args.append(value)
        except SyntaxError as e:
            raise TemplateSyntaxError(f"Could not parse argument: {arg}") from e

    # Append extra args to the last portion of the parsed function
    if parsed_function.portions:
        parsed_function.portions[-1].args.extend(extra_args)

    return ViewNode(parsed_function, context_variable_name)
