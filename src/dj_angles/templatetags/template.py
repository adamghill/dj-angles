import logging

from django.template import Node, NodeList, TemplateSyntaxError

from dj_angles.evaluator import ParsedFunction
from dj_angles.tokenizer import yield_tokens

logger = logging.getLogger(__name__)


class NodeListRenderer:
    def __init__(self, nodelist: NodeList, parsed_function: ParsedFunction, *, include_context: bool = False):
        self.nodelist = nodelist
        self.parsed_function = parsed_function
        self.include_context = include_context

    def render(self, context: dict) -> str:
        return str(self.nodelist.render(context))


class TemplateNode(Node):
    def __init__(self, nodelist: NodeList, parsed_function: ParsedFunction, *, include_context: bool = False):
        self.nodelist = nodelist
        self.parsed_function = parsed_function
        self.include_context = include_context

    def render(self, context):
        """Execute the function with the provided arguments and stores the results in context."""

        if len(self.parsed_function.portions) > 1:
            raise TemplateSyntaxError("Invalid template renderer")

        last_portion = self.parsed_function.portions[-1]

        context.push(
            {
                last_portion.name: NodeListRenderer(
                    self.nodelist, self.parsed_function, include_context=self.include_context
                )
            }
        )

        # Must render a string
        return ""


def do_template(parser, token) -> TemplateNode:
    """Parses the token to get all the pieces needed to render the template.

    Args:
        parser: The template parser.
        token: The token to parse.

    Returns:
        TemplateNode: Handles rendering the template.
    """

    # Get the nodelist up until the endtemplate tag
    nodelist = parser.parse(("endtemplate",))
    parser.delete_first_token()

    """
    Split the contents by whitespace. Examples:
        - "template some_function(arg1, arg2)"
    """
    contents = list(yield_tokens(token.contents, " ", handle_quotes=True, handle_parenthesis=True))

    # The first content is always the name of the tag, so pop it off
    contents.pop(0)

    if len(contents) < 1:
        raise TemplateSyntaxError("template requires at least 1 argument")

    parsed_function = ParsedFunction(contents[0])

    include_context = False

    if len(contents) == 3 and contents[1] == "with" and contents[2] == "context":  # noqa: PLR2004
        include_context = True

    return TemplateNode(nodelist, parsed_function, include_context=include_context)
