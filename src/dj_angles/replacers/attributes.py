"""Replace attributes like `<div dj-if="condition">` with Django template tags.

1. Parses HTML into a tree structure
2. Groups conditional elements by their parent (siblings)
3. Chains siblings together (if → elif → else)
4. Generates output with proper {% if %}/{% endif %} wrapping
"""

import re
from dataclasses import dataclass
from typing import Optional

from dj_angles.htmls import VOID_ELEMENTS
from dj_angles.replacers.objects import AtomicEdit, apply_edits
from dj_angles.settings import get_setting


@dataclass
class ConditionalElement:
    """Represents an element with a dj-if/elif/else attribute."""

    type: str  # 'if', 'elif', 'else'
    condition: str  # The condition value (empty for else)
    start_pos: int  # Position of '<' in original HTML
    end_pos: int  # Position after '>' of opening tag
    full_end_pos: int  # Position after closing tag (full element)
    original_tag: str  # The original opening tag
    original_full: str  # The full original element with content
    attr_match: re.Match  # The regex match for the attribute

    # Chain linking (assigned during processing)
    chain_id: int = -1
    next_in_chain: Optional["ConditionalElement"] = None


def replace_attributes(html: str) -> str:
    """Convert dj-if/elif/else attributes to Django template tags.

    Args:
        html: The HTML string to process
        prefix: The attribute prefix (default "dj-"). If None, uses detailed configuration.

    Returns:
        HTML with Django template tags
    """

    prefix = get_setting("initial_attribute_regex", default=r"(dj-)")

    # Step 1: Find ALL conditional elements
    elements = _find_conditional_elements(html, prefix)

    if not elements:
        return html

    # Step 2: Link chains using ALL elements (for proper hierarchy detection)
    _link_chains(elements)

    # Step 3: Compute and apply atomic edits
    return _apply_atomic_edits(elements, html)


def _find_conditional_elements(html: str, prefix: str) -> list[ConditionalElement]:
    """Find all elements with conditional attributes."""

    # Pattern: handle double and single quotes separately for embedded quotes
    # Group 1: attribute name (prefix + type)
    # Named groups v1/v2/v3 used for value to robustly handle capturing groups in prefix
    attr_pattern = (
        rf'\s({prefix}(?:if|elif|else|endif|fi))(?:=(?:"(?P<v1>[^"]*)"|' + r"'(?P<v2>[^']*)'" + r"|(?P<v3>[^\s>]+)))?"
    )

    elements = []

    for match in re.finditer(attr_pattern, html):
        full_attr = match.group(1)

        # Extract type by checking suffix
        if full_attr.endswith("elif"):
            attr_type = "elif"
        elif full_attr.endswith("endif"):
            attr_type = "endif"
        elif full_attr.endswith("else"):
            attr_type = "else"
        elif full_attr.endswith("if"):
            attr_type = "if"
        elif full_attr.endswith("fi"):
            attr_type = "fi"
        else:
            continue

        # Value is in named groups v1 (double), v2 (single), or v3 (unquoted)
        condition = match.group("v1") or match.group("v2") or match.group("v3") or ""

        # Find the start of the containing tag
        tag_start = html.rfind("<", 0, match.start())

        # Find the end of the opening tag
        tag_end = html.find(">", match.end()) + 1

        # Find the element's full extent (including closing tag)
        full_end = _find_element_end(html, tag_start, tag_end)

        elements.append(
            ConditionalElement(
                type=attr_type,
                condition=condition,
                start_pos=tag_start,
                end_pos=tag_end,
                full_end_pos=full_end,
                original_tag=html[tag_start:tag_end],
                original_full=html[tag_start:full_end],
                attr_match=match,
            )
        )

    # Sort by position
    elements.sort(key=lambda e: e.start_pos)

    return elements


def _find_element_end(html: str, tag_start: int, tag_end: int) -> int:
    """Find the end position of an element (after its closing tag)."""

    # Get the tag name
    tag_html = html[tag_start:tag_end]
    tag_match = re.match(r"<(\w+)", tag_html)

    if not tag_match:
        return tag_end

    tag_name = tag_match.group(1)

    # Check for self-closing or void elements
    if tag_html.rstrip().endswith("/>"):
        return tag_end

    if tag_name.lower() in VOID_ELEMENTS:
        return tag_end

    # Find matching closing tag, counting nesting
    depth = 1
    pos = tag_end
    pattern = re.compile(rf"<(/)?{tag_name}(?:\s[^>]*)?\s*/?>", re.IGNORECASE)

    while depth > 0 and pos < len(html):
        m = pattern.search(html, pos)

        if not m:
            break

        if m.group(1):  # Closing tag
            depth -= 1
        elif not m.group(0).endswith("/>"):  # Opening tag (not self-closing)
            depth += 1

        pos = m.end()

    return pos


def _link_chains(elements: list[ConditionalElement]) -> None:
    """Link if-elif-else elements into chains based on sibling relationships.

    Two elements are siblings if:
    1. Neither is contained within the other
    2. They are not separated by a non-conditional sibling (for simplicity,
       we just check that elif/else immediately follows the previous in chain)
    """

    chain_id = 0

    for i, elem in enumerate(elements):
        if elem.type == "if":
            elem.chain_id = chain_id
            chain_id += 1

        elif elem.type in ("elif", "else"):
            match = _find_preceding_sibling(elem, elements[:i])

            if match:
                elem.chain_id = match.chain_id
                match.next_in_chain = elem
            else:
                # Throw AssertionError for orphaned elif/else
                attr_name = elem.attr_match.group(1)

                raise AssertionError(f"Invalid use of {attr_name} attribute")


def _find_preceding_sibling(
    elem: ConditionalElement, candidates: list[ConditionalElement]
) -> ConditionalElement | None:
    """Find the if/elif that this elif/else belongs to."""

    for candidate in reversed(candidates):
        if candidate.type not in ("if", "elif"):
            continue

        if candidate.next_in_chain is not None:
            continue

        # Key check: candidate's full element must END before this starts
        # This means they're siblings, not parent-child
        if candidate.full_end_pos <= elem.start_pos:
            # Additional check: candidate must not be inside another element
            # that our else is OUTSIDE of (meaning different hierarchy levels)
            is_nested_inside_other = False

            for other in candidates:
                if other is candidate:
                    continue

                # If candidate is inside 'other', and elem is outside 'other'
                if other.start_pos < candidate.start_pos < other.full_end_pos and elem.start_pos >= other.full_end_pos:
                    is_nested_inside_other = True

                    break

            if not is_nested_inside_other:
                return candidate

    return None


def _apply_atomic_edits(elements: list[ConditionalElement], html: str) -> str:
    """Compute and apply atomic edits for all elements."""

    edits: list[AtomicEdit] = []

    for elem in elements:
        # Check if attribute is on a closing tag (e.g. </div dj-endif>)
        is_closing_tag = elem.original_tag.startswith("</")

        # 1. Insert template start tag
        start_tag = ""

        if is_closing_tag and elem.type in ("endif", "fi"):
            # Don't emit {% endif %} for closing tags, just clean them.
            # The chain logic will handle the automatic closing after this tag.
            start_tag = ""
        elif elem.type == "if":
            start_tag = f"{{% if {elem.condition} %}}"
        elif elem.type == "elif":
            start_tag = f"{{% elif {elem.condition} %}}"
        elif elem.type == "else":
            start_tag = "{% else %}"
        elif elem.type in {"endif", "fi"}:
            start_tag = "{% endif %}"
        else:
            continue

        if start_tag:
            edits.append(AtomicEdit(position=elem.start_pos, content=start_tag))

        # 2. Remove the attribute (replace with cleaned tag)
        new_tag = _remove_attribute(elem.original_tag, elem.attr_match, elem.start_pos)
        edits.append(AtomicEdit(position=elem.start_pos, content=new_tag, is_insert=False, end_position=elem.end_pos))

        # 3. Insert endif if needed
        # Logic: If no next element in chain, AND it's a structural tag (if/elif/else), add endif.
        should_add_endif = elem.next_in_chain is None and elem.type in ("if", "elif", "else")

        if should_add_endif:
            edits.append(AtomicEdit(position=elem.full_end_pos, content="{% endif %}"))

    return apply_edits(html, edits)


def _remove_attribute(tag: str, attr_match: re.Match, tag_start: int) -> str:
    """Remove the conditional attribute from an opening tag."""

    # Calculate position within tag
    attr_start_in_tag = attr_match.start() - tag_start
    attr_end_in_tag = attr_match.end() - tag_start

    new_tag = tag[:attr_start_in_tag] + tag[attr_end_in_tag:]

    # Clean up extra spaces
    new_tag = re.sub(r"\s+>", ">", new_tag)
    new_tag = re.sub(r"\s{2,}", " ", new_tag)

    return new_tag
