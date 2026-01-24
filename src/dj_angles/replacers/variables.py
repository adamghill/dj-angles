import logging
import re

from dj_angles.replacers.objects import AtomicEdit, apply_edits
from dj_angles.strings import dequotify
from dj_angles.tokenizer import yield_tokens

logger = logging.getLogger(__name__)


def replace_variables(html: str) -> str:
    """Replace Django-like tags (or-expressions and inline-ifs) with standard Django tags.

    Args:
        html: Template HTML.

    Returns:
        The converted template HTML.
    """

    edits: list[AtomicEdit] = []

    # Find all {{ ... }} blocks
    # We use a pattern that matches content inside braces, respecting quotes to allow '}' inside strings
    # This matches:
    # 1. Any character that is NOT a quote or brace
    # 2. OR a single-quoted string
    # 3. OR a double-quoted string
    # All repeated until we see '}}'
    variable_pattern = r"""\{\{((?:[^'\"{}]+|'[^']*'|"[^"]*")*?)\}\}"""

    for match in re.finditer(variable_pattern, html):
        original = match.group(0)
        content = match.group(1).strip()

        # Parse the content into tokens, respecting quotes
        # We use space as the breaking character to tokenize words/symbols
        tokens = list(yield_tokens(content, breaking_character=" "))
        tokens = [t.strip() for t in tokens if t.strip()]

        if not tokens:
            continue

        # Check for ternary: "A if B else C"
        if "if" in tokens and "else" in tokens:
            if_index = tokens.index("if")
            else_index = tokens.index("else")

            # Ensure "if" comes before "else"
            # And that we have operands: A if B else C
            # A (true_value) must exist (index > 0)
            # B (condition) must exist (between if and else)
            # C (false_value) must exist (after else)
            if if_index < else_index and if_index > 0 and (else_index - if_index > 1) and else_index < len(tokens) - 1:
                true_value = " ".join(tokens[:if_index])
                condition = " ".join(tokens[if_index + 1 : else_index])
                false_value = " ".join(tokens[else_index + 1 :])

                # Helper to determine if a value should be wrapped in {{ }} or raw
                def process_value(val: str) -> str:
                    dequoted = dequotify(val)
                    is_quoted = val != dequoted

                    if not is_quoted:
                        # It's a variable, so wrap it
                        return f"{{{{ {val} }}}}"
                    else:
                        # If it contains template syntax characters, wrap it in verbatim
                        if "{" in dequoted or "}" in dequoted or "%" in dequoted:
                            return f"{{% verbatim %}}{dequoted}{{% endverbatim %}}"
                        # Otherwise return raw string for cleaner template
                        return dequoted

                true_value_final = process_value(true_value)
                false_value_final = process_value(false_value)

                replacement = f"{{% if {condition} %}}{true_value_final}{{% else %}}{false_value_final}{{% endif %}}"

                edits.append(
                    AtomicEdit(
                        position=match.start(),
                        content=replacement,
                        is_insert=False,
                        end_position=match.end(),
                    )
                )
                # Skip 'or' check if we matched a ternary
                continue

        # Check for 'or': "A or B"
        if "or" in tokens:
            or_index = tokens.index("or")

            # Check for operands: A or B
            if or_index > 0 and or_index < len(tokens) - 1:
                variable_part = " ".join(tokens[:or_index])
                default_value = " ".join(tokens[or_index + 1 :])

                def process_value(val: str) -> str:
                    dequoted = dequotify(val)
                    is_quoted = val != dequoted

                    if not is_quoted:
                        return f"{{{{ {val} }}}}"
                    else:
                        if "{" in dequoted or "}" in dequoted or "%" in dequoted:
                            return f"{{% verbatim %}}{dequoted}{{% endverbatim %}}"
                        return dequoted

                default_value_final = process_value(default_value)

                replacement = (
                    f"{{% if {variable_part} %}}{{{{ {variable_part} }}}}{{% else %}}{default_value_final}{{% endif %}}"
                )

                edits.append(
                    AtomicEdit(
                        position=match.start(),
                        content=replacement,
                        is_insert=False,
                        end_position=match.end(),
                    )
                )

    return apply_edits(html, edits)
