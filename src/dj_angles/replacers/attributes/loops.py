import re
from functools import cache

from dj_angles.htmls import VOID_ELEMENTS
from dj_angles.replacers.attributes.elements import Element, ForElement
from dj_angles.replacers.objects import AtomicEdit, apply_edits
from dj_angles.settings import get_setting


@cache
def _for_attr_pattern(prefix: str) -> str:
    """Build and cache the for-loop attribute regex pattern for a given prefix."""
    return (
        rf'\s({prefix}(?:for|empty|endfor))(?:=(?:"(?P<double_quote>[^"]*)"|'
        r"'(?P<single_quote>[^']*)'"
        r"|(?P<unquoted>[^\s>]+)))?"
    )


def replace_loops(html: str) -> str:
    """Convert dj-for/dj-empty/dj-endfor attributes to Django template tags.

    Args:
        html: The HTML string to process.

    Returns:
        HTML with Django template tags for for-loops.
    """

    prefix = get_setting("initial_attribute_regex", default=r"(dj-)")
    attr_pattern = _for_attr_pattern(prefix)
    elements: list[ForElement] = []

    for match in re.finditer(attr_pattern, html):
        full_attr = match.group(1)

        if full_attr.endswith("endfor"):
            attr_type = "endfor"
        elif full_attr.endswith("empty"):
            attr_type = "empty"
        elif full_attr.endswith("for"):
            attr_type = "for"
        else:
            continue

        expression = match.group("double_quote") or match.group("single_quote") or match.group("unquoted") or ""

        if attr_type == "for" and not expression:
            attr_name = match.group(1)
            raise AssertionError(f"{attr_name} attribute must have a value")

        if attr_type == "for" and match.group("unquoted"):
            attr_name = match.group(1)
            raise AssertionError(f"{attr_name} attribute value must be quoted")

        base = Element.from_match(html, match, attr_type)
        elements.append(
            ForElement(
                tag_name=base.tag_name,
                tag_start=base.tag_start,
                tag_end=base.tag_end,
                full_end=base.full_end,
                original_tag=base.original_tag,
                original_full=base.original_full,
                attr_match=match,
                type=attr_type,
                value=expression,
            )
        )

    if not elements:
        return html

    elements.sort(key=lambda e: e.tag_start)
    _link_for_chains(elements)

    edits: list[AtomicEdit] = []

    for elem in elements:
        is_closing_tag = elem.original_tag.startswith("</")

        if elem.type == "for":
            edits.append(AtomicEdit(position=elem.tag_start, content=f"{{% for {elem.value} %}}"))

            cleaned_tag = elem.remove_attribute()
            cleaned_tag = re.sub(r"\s*/>$", ">", cleaned_tag)
            edits.append(
                AtomicEdit(position=elem.tag_start, content=cleaned_tag, is_insert=False, end_position=elem.tag_end)
            )

            original_was_self_closing = (
                elem.original_tag.rstrip().endswith("/>") or elem.tag_name.lower() in VOID_ELEMENTS
            )
            if original_was_self_closing:
                closing = f"</{elem.tag_name}>"
                if elem.empty_sibling is None:
                    edits.append(AtomicEdit(position=elem.tag_end, content=f"{closing}{{% endfor %}}"))
                else:
                    edits.append(AtomicEdit(position=elem.tag_end, content=closing))
            elif elem.empty_sibling is None:
                has_explicit_endfor = any(
                    e.type == "endfor" and elem.tag_start < e.tag_start < elem.full_end
                    for e in elements
                    if e is not elem
                )
                if not has_explicit_endfor:
                    edits.append(AtomicEdit(position=elem.full_end, content="{% endfor %}"))

        elif elem.type == "empty":
            edits.append(AtomicEdit(position=elem.tag_start, content="{% empty %}"))
            cleaned_tag = elem.remove_attribute()
            cleaned_tag = re.sub(r"\s*/>$", ">", cleaned_tag)
            edits.append(
                AtomicEdit(position=elem.tag_start, content=cleaned_tag, is_insert=False, end_position=elem.tag_end)
            )
            edits.append(AtomicEdit(position=elem.full_end, content="{% endfor %}"))

        elif elem.type == "endfor":
            if is_closing_tag:
                cleaned_tag = elem.remove_attribute()
                edits.append(
                    AtomicEdit(
                        position=elem.tag_start,
                        content=cleaned_tag,
                        is_insert=False,
                        end_position=elem.tag_end,
                    )
                )
                edits.append(AtomicEdit(position=elem.tag_end, content="{% endfor %}"))
            else:
                edits.append(AtomicEdit(position=elem.tag_start, content="{% endfor %}"))
                cleaned_tag = elem.remove_attribute()
                edits.append(
                    AtomicEdit(position=elem.tag_start, content=cleaned_tag, is_insert=False, end_position=elem.tag_end)
                )

    return apply_edits(html, edits)


def _link_for_chains(elements: list[ForElement]) -> None:
    """Link dj-empty elements to their preceding dj-for sibling."""

    for i, elem in enumerate(elements):
        if elem.type != "empty":
            continue

        for candidate in reversed(elements[:i]):
            if candidate.type != "for":
                continue
            if candidate.empty_sibling is not None:
                continue
            if candidate.full_end <= elem.tag_start:
                candidate.empty_sibling = elem
                break
        else:
            attr_name = elem.attr_match.group(1)
            raise AssertionError(f"Invalid use of {attr_name} attribute without a preceding dj-for")
