"""AST-based attribute replacement using minestrone.

This module provides an alternative to regex-based dj-if/dj-else processing
by using proper HTML parsing to handle nested conditionals correctly.
"""

import logging
from dataclasses import dataclass, field
from typing import Optional

from minestrone import HTML, Element

from dj_angles.replacers.objects import Replacement
from dj_angles.settings import get_setting

logger = logging.getLogger(__name__)


@dataclass
class ConditionalElement:
    """Represents a conditional element (if/elif/else) in the AST."""

    type: str  # 'if', 'elif', 'else'
    condition: str
    element: Element
    depth: int = 0  # Nesting depth
    chain_id: int = 0  # Which if-elif-else chain this belongs to
    matched_if: Optional["ConditionalElement"] = None  # The if this elif/else belongs to


def get_attribute_replacements_ast(html: str) -> list[Replacement]:
    """Get attribute replacements using AST-based parsing.

    This handles nested conditionals correctly by using the DOM tree structure
    rather than regex-based position matching.
    """
    initial_attr = get_setting("initial_attribute_regex", default=r"(dj-)")
    # Extract the prefix (e.g., "dj-" from "(dj-)")
    prefix = initial_attr.strip("()")

    if_attr = f"{prefix}if"
    elif_attr = f"{prefix}elif"
    else_attr = f"{prefix}else"
    endif_attr = f"{prefix}endif"
    fi_attr = f"{prefix}fi"

    parsed_html = HTML(html)
    replacements = []

    # Collect all conditional elements with their parent relationships
    conditionals = []

    # Find all if elements
    for el in parsed_html.query(f"[{if_attr}]"):
        conditionals.append(
            ConditionalElement(
                type="if",
                condition=el.attributes.get(if_attr, ""),
                element=el,
            )
        )

    # Find all elif elements
    for el in parsed_html.query(f"[{elif_attr}]"):
        conditionals.append(
            ConditionalElement(
                type="elif",
                condition=el.attributes.get(elif_attr, ""),
                element=el,
            )
        )

    # Find all else elements
    for el in parsed_html.query(f"[{else_attr}]"):
        conditionals.append(
            ConditionalElement(
                type="else",
                condition="",
                element=el,
            )
        )

    # Sort by document order (using HTML position)
    # We need to track position in original HTML using the specific attribute
    def get_position(cond: ConditionalElement) -> int:
        """Get position of element's conditional attribute in HTML."""
        attr_name = f"{prefix}{cond.type}"
        if cond.condition:
            # Look for the full attribute with value
            search_str = f'{attr_name}="{cond.condition}"'
        else:
            # For dj-else, look for the attribute name followed by either > or space
            # Find all occurrences and return the appropriate one based on parent
            search_str = f"{attr_name}"
        pos = html.find(search_str)
        return pos if pos >= 0 else 999999

    conditionals.sort(key=get_position)

    # Debug: print order
    logger.debug("Conditionals order:")
    for i, c in enumerate(conditionals):
        logger.debug(
            f"  {i}: {c.type}={c.condition} at pos {get_position(c)}, parent={c.element.parent.name if c.element.parent and hasattr(c.element.parent, 'name') else c.element.parent}"
        )

    # Assign depths based on parent relationships and match chains
    chain_id = 0
    if_stack = []  # Stack of open if statements

    for cond in conditionals:
        if cond.type == "if":
            # Check nesting by looking at parent
            parent = cond.element.parent
            parent_depth = 0

            # Find if this if is nested inside another conditional element
            for prev_cond in if_stack:
                if _is_ancestor(prev_cond.element, cond.element):
                    parent_depth = prev_cond.depth + 1
                    break

            cond.depth = parent_depth
            cond.chain_id = chain_id
            chain_id += 1
            if_stack.append(cond)

        elif cond.type in ["elif", "else"]:
            # Find the matching if - it should be:
            # 1. A sibling (same parent)
            # 2. The most recent if at the same parent level
            matched = _find_matching_if(cond, conditionals, if_stack)

            if matched:
                cond.depth = matched.depth
                cond.chain_id = matched.chain_id
                cond.matched_if = matched
            else:
                logger.warning(f"Could not find matching if for {cond.type} element")
                continue

    # Generate replacements
    processed_chains = set()  # Track which chains we've processed

    for cond in conditionals:
        el = cond.element
        tag_string = el.tag_string

        # Build the conditional template tag
        if cond.type == "if":
            prefix_tag = f"{{% if {cond.condition} %}}"
            suffix_tag = "{% endif %}"
        elif cond.type == "elif":
            prefix_tag = f"{{% elif {cond.condition} %}}"
            suffix_tag = "{% endif %}"
        elif cond.type == "else":
            prefix_tag = "{% else %}"
            suffix_tag = "{% endif %}"
        else:
            continue

        # Remove the dj-* attribute from the opening tag
        attr_name = f"{prefix}{cond.type}"
        attr_pattern = f'{attr_name}="{cond.condition}"' if cond.condition else f"{attr_name}"
        new_tag_string = tag_string.replace(attr_pattern, "").replace('=""', "").replace("  ", " ").rstrip()
        if new_tag_string.endswith(" >"):
            new_tag_string = new_tag_string[:-2] + ">"

        # Build original and replacement HTML
        original_html = str(el)
        closing_tag = el.closing_tag_string if hasattr(el, "closing_tag_string") and el.closing_tag_string else ""

        # Get inner content
        inner_html = original_html[len(tag_string) :]
        if closing_tag:
            inner_html = inner_html[: -len(closing_tag)]

        # Determine if we need endif
        # - If next sibling is elif/else in same chain, don't add endif
        # - Otherwise, add endif
        needs_endif = True
        for next_cond in conditionals:
            if next_cond.chain_id == cond.chain_id and next_cond != cond:
                pos_current = get_position(cond)
                pos_next = get_position(next_cond)
                if pos_next > pos_current and next_cond.type in ["elif", "else"]:
                    needs_endif = False
                    break

        final_suffix = suffix_tag if needs_endif else ""
        replacement_html = f"{prefix_tag}{new_tag_string}{inner_html}{closing_tag}{final_suffix}"

        # Create Tag object for compatibility
        from dj_angles.tags import Tag

        tag = Tag(
            tag_map={},
            html=tag_string,
            tag_name=el.name,
            template_tag_args="",
        )
        tag.outer_html = original_html

        replacement = Replacement(
            original=original_html,
            replacement=replacement_html,
            tag=tag,
            keep_endif=needs_endif,
            tag_start_idx=get_position(cond),
        )
        replacements.append(replacement)

    return replacements


def _is_ancestor(potential_ancestor: Element, element: Element) -> bool:
    """Check if potential_ancestor is an ancestor of element."""
    current = element.parent
    while current:
        if current == potential_ancestor:
            return True
        current = current.parent if hasattr(current, "parent") else None
    return False


def _find_matching_if(
    cond: ConditionalElement,
    all_conditionals: list[ConditionalElement],
    if_stack: list[ConditionalElement],
) -> Optional[ConditionalElement]:
    """Find the matching if statement for an elif/else.There are no lints to fix.

    Uses a simple rule: the matching if is the most recent if
    where the else/elif appears AFTER the if's closing tag (siblings)
    rather than inside the if's content (nested).
    """
    else_element_html = str(cond.element)

    # Look backwards through the if stack
    for if_cond in reversed(if_stack):
        if_element_html = str(if_cond.element)

        # If the else appears INSIDE the if's HTML, they're NOT siblings
        # (the else would be for a nested if already in the if_stack)
        if else_element_html in if_element_html:
            continue

        # They're siblings - this is the match!
        return if_cond

    return None


# For testing
if __name__ == "__main__":
    test_html = """<div dj-if="outer">
  <div dj-if="inner">
    <p>Inner true</p>
  </div>
  <div dj-else>
    <p>Inner false</p>
  </div>
</div>
<div dj-else>
  <p>Outer false</p>
</div>"""

    import os

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example.project.settings")

    import django

    django.setup()

    replacements = get_attribute_replacements_ast(test_html)

    print("Replacements:")
    for r in replacements:
        print(f"\n  Original: {r.original[:60]}...")
        print(f"  Replacement: {r.replacement[:60]}...")
