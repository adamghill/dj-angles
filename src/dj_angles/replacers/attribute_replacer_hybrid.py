"""Hybrid approach: AST for analysis, position-based regex for replacement.

This combines the best of both worlds:
- minestrone for understanding HTML structure and parent/child relationships
- regex with position tracking for accurate string replacement
"""

import logging
import re
from dataclasses import dataclass
from typing import List, Tuple

from minestrone import HTML

from dj_angles.replacers.objects import Replacement
from dj_angles.settings import get_setting

logger = logging.getLogger(__name__)


@dataclass
class ConditionalMatch:
    """A dj-* attribute match with position information."""

    type: str  # 'if', 'elif', 'else', 'endif', 'fi'
    condition: str  # The condition value
    attr_start: int  # Start position of attribute in HTML
    attr_end: int  # End position of attribute in HTML
    tag_start: int  # Start position of the containing tag
    tag_end: int  # End position of the containing tag (just the opening tag, not inner HTML)
    full_match: str  # The full attribute match string
    chain_id: int = -1  # Which if-elif-else chain this belongs to
    matched_if_idx: int = -1  # Index of the matching if for elif/else


def get_attribute_replacements_hybrid(html: str) -> list[Replacement]:
    """Get attribute replacements using hybrid AST + position approach."""
    initial_attr = get_setting("initial_attribute_regex", default=r"(dj-)")
    prefix = initial_attr.strip("()")

    # Step 1: Find all dj-* attributes with exact positions
    # Uses backreference for matching quotes
    attr_pattern = rf"\s({prefix}(?:if|elif|else|endif|fi))(?:=(?:(['\"])([^'\"]*?)\2|([^\s>]+)))?"
    matches: List[ConditionalMatch] = []

    for m in re.finditer(attr_pattern, html):
        attr_type = m.group(1).replace(prefix, "")  # 'if', 'elif', 'else', etc.
        # Value is in group 3 (quoted) or group 4 (unquoted)
        condition = m.group(3) if m.group(3) is not None else (m.group(4) or "")

        # Find the containing tag's start
        tag_start = html.rfind("<", 0, m.start())
        # Find the tag's end (the >)
        tag_end = html.find(">", m.end()) + 1

        matches.append(
            ConditionalMatch(
                type=attr_type,
                condition=condition,
                attr_start=m.start(),
                attr_end=m.end(),
                tag_start=tag_start,
                tag_end=tag_end,
                full_match=m.group(0),
            )
        )

    if not matches:
        return []

    # Step 2: Use AST to determine parent/sibling relationships for if-else matching
    # Key insight: an else is a sibling of its if if the else tag is NOT inside the if tag's HTML
    _assign_chains(matches, html)

    # Step 3: Build replacements with correct endif placement
    return _build_replacements(matches, html, prefix)


def _assign_chains(matches: List[ConditionalMatch], html: str) -> None:
    """Assign chain IDs to match if-elif-else blocks correctly."""
    chain_id = 0
    if_stack = []  # Stack of (match_idx, if_match) for open ifs

    for i, match in enumerate(matches):
        if match.type == "if":
            match.chain_id = chain_id
            # Push this if onto the stack with its HTML extent
            # Find the full extent - we need the closing tag
            # For now, use position-based heuristic
            if_stack.append((i, match))
            chain_id += 1

        elif match.type in ["elif", "else"]:
            # Find matching if: walk backwards to find an if that this is a sibling of
            matched = _find_matching_if(match, matches, if_stack, html)
            if matched is not None:
                match.matched_if_idx = matched
                match.chain_id = matches[matched].chain_id
            else:
                logger.warning(f"Could not find matching if for {match.type} at position {match.attr_start}")

        elif match.type in ["endif", "fi"]:
            # Explicit endif closes the most recent if
            if if_stack:
                closed_idx, _ = if_stack.pop()
                match.matched_if_idx = closed_idx
                match.chain_id = matches[closed_idx].chain_id


def _find_matching_if(
    match: ConditionalMatch,
    all_matches: List[ConditionalMatch],
    if_stack: List[Tuple[int, ConditionalMatch]],
    html: str,
) -> int | None:
    """Find the index of the matching if for an elif/else."""
    # Get the HTML from the start of this else/elif tag to find context
    current_pos = match.tag_start

    # Walk backwards through the if stack
    # The matching if is the one where we are NOT inside its full HTML extent
    for idx, if_match in reversed(if_stack):
        # Check if this else/elif appears INSIDE the if's full HTML
        # We need to find where the if's content ends
        # Quick heuristic: Find the if's element extent using the HTML structure

        # Get the tag name for the if
        tag_match = re.match(r"<(\w+)", html[if_match.tag_start :])
        if tag_match:
            tag_name = tag_match.group(1)
            # Find closing tag of the if element
            # This is a simplified approach - we look for our else/elif position
            # relative to the if's content
            if_html_start = if_match.tag_start

            # Find the corresponding closing tag
            # We need to count nested tags of the same name
            depth = 1
            pos = if_match.tag_end
            close_pattern = re.compile(rf"</?{tag_name}(?:\s[^>]*)?\s*/?>", re.IGNORECASE)

            while depth > 0 and pos < len(html):
                m = close_pattern.search(html, pos)
                if not m:
                    break
                if m.group(0).startswith("</"):
                    depth -= 1
                elif not m.group(0).endswith("/>"):  # Not self-closing
                    depth += 1
                pos = m.end()

            if_html_end = pos  # End of the if element's full HTML

            # If our else/elif is AFTER the if's full HTML, they're siblings
            if current_pos >= if_html_end:
                return idx
            # If our else/elif is INSIDE the if's full HTML, it's for a nested if
            # Continue searching for an outer if

    return None


def _build_replacements(
    matches: List[ConditionalMatch],
    html: str,
    prefix: str,
) -> list[Replacement]:
    """Build replacements from the analyzed matches."""
    from dj_angles.tags import Tag

    replacements = []

    # Track which chains have their endif removed (because there's an elif/else following)
    chain_needs_endif = {m.chain_id: True for m in matches if m.type == "if"}

    # Mark chains that have elif or else - the if should not have endif
    for m in matches:
        if m.type in ["elif", "else"] and m.matched_if_idx >= 0:
            chain_needs_endif[m.chain_id] = False

    for match in matches:
        if match.type in ["endif", "fi"]:
            # Handle explicit endif - remove the attribute and add {% endif %}
            tag_html = html[match.tag_start : match.tag_end]
            # Remove the dj-endif/dj-fi attribute
            new_tag = tag_html[: match.attr_start - match.tag_start] + tag_html[match.attr_end - match.tag_start :]
            new_tag = new_tag.replace("  ", " ")
            if new_tag.endswith(" >"):
                new_tag = new_tag[:-2] + ">"

            replacement_html = new_tag + "{% endif %}"

            tag = Tag(tag_map={}, html=tag_html, tag_name="", template_tag_args="")
            tag.outer_html = tag_html

            replacements.append(
                Replacement(
                    original=tag_html,
                    replacement=replacement_html,
                    tag=tag,
                    keep_endif=True,
                    tag_start_idx=match.tag_start,
                )
            )
            continue

        # Build conditional start tag
        if match.type == "if":
            cond_start = f"{{% if {match.condition} %}}"
            cond_end = "{% endif %}"
        elif match.type == "elif":
            cond_start = f"{{% elif {match.condition} %}}"
            cond_end = "{% endif %}"
        elif match.type == "else":
            cond_start = "{% else %}"
            cond_end = "{% endif %}"
        else:
            continue

        # Get the full element HTML (opening tag + content + closing tag)
        tag_html = html[match.tag_start : match.tag_end]

        # Remove the dj-* attribute from the tag
        new_tag = tag_html[: match.attr_start - match.tag_start] + tag_html[match.attr_end - match.tag_start :]
        new_tag = new_tag.replace("  ", " ")
        if new_tag.endswith(" >"):
            new_tag = new_tag[:-2] + ">"

        # Find the element's full extent (including content and closing tag)
        tag_match = re.match(r"<(\w+)", tag_html)
        if tag_match:
            tag_name = tag_match.group(1)

            # Find closing tag
            depth = 1
            pos = match.tag_end
            close_pattern = re.compile(rf"</?{tag_name}(?:\s[^>]*)?\s*/?>", re.IGNORECASE)

            while depth > 0 and pos < len(html):
                m = close_pattern.search(html, pos)
                if not m:
                    break
                if m.group(0).startswith("</"):
                    depth -= 1
                elif not m.group(0).endswith("/>"):
                    depth += 1
                pos = m.end()

            element_end = pos
        else:
            element_end = match.tag_end

        # Get full original element
        original_html = html[match.tag_start : element_end]
        inner_content = html[match.tag_end : element_end - len(f"</{tag_name}>") if tag_name else element_end]
        closing = html[element_end - len(f"</{tag_name}>") : element_end] if tag_name else ""

        # Build replacement
        # Check if this element needs an endif
        needs_endif = (match.type == "if" and chain_needs_endif.get(match.chain_id, True)) or (
            match.type in ["elif", "else"]
        )

        # But if there's a following elif/else in the same chain, don't add endif
        for later_match in matches:
            if later_match.chain_id == match.chain_id and later_match.attr_start > match.attr_start:
                if later_match.type in ["elif", "else"]:
                    needs_endif = False
                    break

        replacement_html = cond_start + new_tag + inner_content + closing
        if needs_endif:
            replacement_html += cond_end

        tag = Tag(tag_map={}, html=tag_html, tag_name=tag_name or "", template_tag_args="")
        tag.outer_html = original_html

        replacements.append(
            Replacement(
                original=original_html,
                replacement=replacement_html,
                tag=tag,
                keep_endif=needs_endif,
                tag_start_idx=match.tag_start,
            )
        )

    return replacements


if __name__ == "__main__":
    import os

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example.project.settings")

    import django

    django.setup()

    test_html = """<span dj-if='False'>test</span>"""

    replacements = get_attribute_replacements_hybrid(test_html)
    print("Test 1 - Simple if:")
    for r in replacements:
        print(f"  Original: {r.original}")
        print(f"  Replacement: {r.replacement}")

    print()
    test_html2 = """<div dj-if="outer">
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

    replacements2 = get_attribute_replacements_hybrid(test_html2)
    print("Test 2 - Nested same-tag:")
    for r in replacements2:
        print(f"  Original: {r.original[:40]}...")
        print(f"  Replacement: {r.replacement[:40]}...")
        print()
