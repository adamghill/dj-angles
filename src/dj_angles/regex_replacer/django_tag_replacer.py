import logging
import re

from dj_angles.regex_replacer.objects import Replacement
from dj_angles.strings import dequotify
from dj_angles.tags import Tag

logger = logging.getLogger(__name__)


def get_django_tag_replacements(html: str) -> list[Replacement]:
    """Get a list of django tag replacements based on the template HTML.

    Args:
        param html: Template HTML.

    Returns:
        A list of `Replacement` where `original` is the existing element, e.g. "{{ blob or 'hello' }}"
        and `replacement` is the replacement string, e.g. "{% if blob %}{{ blob }}{% else %}'hello'{% endif %}".
    """

    replacements: list[Replacement] = []

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

        # Create a minimal Tag object for the replacement
        # The actual tag content isn't critical for this replacement
        tag = Tag(html=original)

        replacements.append(
            Replacement(original=original, replacement=replacement, tag=tag, tag_start_idx=or_match.start())
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

        # Create a minimal Tag object for the replacement
        tag = Tag(html=original)

        replacements.append(
            Replacement(original=original, replacement=replacement, tag=tag, tag_start_idx=ternary_match.start())
        )

    return replacements
