import logging
import re

from dj_angles.replacers.objects import AtomicEdit, apply_edits
from dj_angles.strings import dequotify

logger = logging.getLogger(__name__)


def replace_variables(html: str) -> str:
    """Replace Django-like tags (or-expressions and inline-ifs) with standard Django tags.

    Args:
        html: Template HTML.

    Returns:
        The converted template HTML.
    """

    edits: list[AtomicEdit] = []

    # Match Django template variables with 'or' expressions
    # This matches or_patterns like {{ var or "default" }} or {{ var|filter or default_value }}
    or_pattern = r"\{\{([^{}]+)\s+or\s+([^{}]+)\}\}"

    for or_match in re.finditer(or_pattern, html):
        original = or_match.group(0)
        variable_part = or_match.group(1).strip()

        default_value = or_match.group(2).strip()
        default_value = dequotify(default_value)

        # Try to handle `{{ 'a or b' }}` which the regex can't deal with easily
        if variable_part.startswith("'") or variable_part.startswith('"'):
            initial_char = variable_part[0]

            if (
                not variable_part.endswith(initial_char)
                and not default_value.startswith(initial_char)
                and default_value.endswith(initial_char)
            ):
                continue

        if default_value == or_match.group(2).strip():
            default_value = f"{{{{ {default_value} }}}}"

        # Create the replacement with if/else logic
        replacement = f"{{% if {variable_part} %}}{{{{ {variable_part} }}}}{{% else %}}{default_value}{{% endif %}}"

        edits.append(
            AtomicEdit(position=or_match.start(), content=replacement, is_insert=False, end_position=or_match.end())
        )

    # Match Django template variables with a inline if expression
    # This matches patterns like {{ 'true' if var else 'false' }}
    inline_if_pattern = r"\{\{\s*([^{}]+?)\s+if\s+([^{}]+?)\s+else\s+([^{}]+?)\s*\}\}"

    for ternary_match in re.finditer(inline_if_pattern, html):
        original = ternary_match.group(0)
        true_value = ternary_match.group(1).strip()
        condition = ternary_match.group(2).strip()
        false_value = ternary_match.group(3).strip()

        # Dequote the string values if they are quoted
        true_value = dequotify(true_value)

        if true_value == ternary_match.group(1).strip():
            true_value = f"{{{{ {true_value} }}}}"

        false_value = dequotify(false_value)

        if false_value == ternary_match.group(3).strip():
            false_value = f"{{{{ {false_value} }}}}"

        # Create the replacement with if/else logic
        replacement = f"{{% if {condition} %}}{true_value}{{% else %}}{false_value}{{% endif %}}"

        edits.append(
            AtomicEdit(
                position=ternary_match.start(), content=replacement, is_insert=False, end_position=ternary_match.end()
            )
        )

    return apply_edits(html, edits)
