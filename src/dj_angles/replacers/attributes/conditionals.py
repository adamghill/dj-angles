import re
from functools import cache

from dj_angles.replacers.attributes.elements import ConditionalElement, Element
from dj_angles.replacers.objects import AtomicEdit, apply_edits
from dj_angles.settings import get_setting


@cache
def _conditional_attr_pattern(prefix: str) -> str:
    """Build and cache the conditional attribute regex pattern for a given prefix."""
    return (
        rf'\s({prefix}(?:if|elif|else|endif|fi))(?:=(?:"(?P<double_quote>[^"]*)"|'
        r"'(?P<single_quote>[^']*)'"
        r"|(?P<unquoted>[^\s>]+)))?"
    )


def replace_conditionals(html: str) -> str:
    """Convert dj-if/elif/else attributes to Django template tags.

    Args:
        html: The HTML string to process.

    Returns:
        HTML with Django template tags.
    """

    prefix = get_setting("initial_attribute_regex", default=r"(dj-)")
    elements = _find_conditional_elements(html, prefix)

    if not elements:
        return html

    _link_chains(elements)

    return _apply_atomic_edits(elements, html)


def _find_conditional_elements(html: str, prefix: str) -> list[ConditionalElement]:
    """Find all elements with conditional attributes."""

    # Named groups double_quote/single_quote/unquoted used for value to robustly
    # handle capturing groups in prefix
    attr_pattern = _conditional_attr_pattern(prefix)
    elements = []

    for match in re.finditer(attr_pattern, html):
        full_attr = match.group(1)

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

        condition = match.group("double_quote") or match.group("single_quote") or match.group("unquoted") or ""

        if attr_type in ("if", "elif") and match.group("unquoted"):
            attr_name = match.group(1)
            raise AssertionError(f"{attr_name} attribute value must be quoted")

        base = Element.from_match(html, match, attr_type)
        elements.append(
            ConditionalElement(
                tag_name=base.tag_name,
                tag_start=base.tag_start,
                tag_end=base.tag_end,
                full_end=base.full_end,
                original_tag=base.original_tag,
                original_full=base.original_full,
                attr_match=match,
                type=attr_type,
                value=condition,
            )
        )

    elements.sort(key=lambda e: e.tag_start)
    return elements


def _link_chains(elements: list[ConditionalElement]) -> None:
    """Link if-elif-else elements into chains based on sibling relationships."""

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

        if candidate.full_end <= elem.tag_start:
            is_nested_inside_other = False

            for other in candidates:
                if other is candidate:
                    continue

                if other.tag_start < candidate.tag_start < other.full_end and elem.tag_start >= other.full_end:
                    is_nested_inside_other = True
                    break

            if not is_nested_inside_other:
                return candidate

    return None


def _apply_atomic_edits(elements: list[ConditionalElement], html: str) -> str:
    """Compute and apply atomic edits for all elements."""

    edits: list[AtomicEdit] = []

    for elem in elements:
        is_closing_tag = elem.original_tag.startswith("</")

        start_tag = ""

        if is_closing_tag and elem.type in ("endif", "fi"):
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
            edits.append(AtomicEdit(position=elem.tag_start, content=start_tag))

        new_tag = elem.remove_attribute()
        edits.append(AtomicEdit(position=elem.tag_start, content=new_tag, is_insert=False, end_position=elem.tag_end))

        should_add_endif = elem.next_in_chain is None and elem.type in ("if", "elif", "else")

        if should_add_endif:
            edits.append(AtomicEdit(position=elem.full_end, content="{% endif %}"))

    return apply_edits(html, edits)
