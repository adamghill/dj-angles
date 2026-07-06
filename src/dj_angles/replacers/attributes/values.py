import re

from dj_angles.replacers.attributes.elements import Element
from dj_angles.replacers.objects import AtomicEdit, apply_edits
from dj_angles.settings import get_setting


def replace_values(html: str) -> str:
    """Convert `dj-value` attributes to Django variable output.

    The attribute is removed from the opening tag, the element's inner content
    is replaced with `{{ value }}`, and void/self-closing tags are turned into
    paired tags so the value has a place to render.

    Args:
        html: The HTML string to process.

    Returns:
        HTML with `dj-value` attributes replaced by Django template variables.
    """

    prefix = get_setting("initial_attribute_regex", default=r"(dj-)")

    attr_pattern = (
        rf"\s({prefix}value)(?:=(?:\"(?P<double_quote>[^\"]*)\"|"
        r"'(?P<single_quote>[^']*)'"
        r"|(?P<unquoted>[^\s>]+)))?"
    )

    elements: list[Element] = []

    for match in re.finditer(attr_pattern, html):
        condition = match.group("double_quote") or match.group("single_quote") or match.group("unquoted") or ""

        if not condition:
            attr_name = match.group(1)
            raise AssertionError(f"{attr_name} attribute must have a value")

        if match.group("unquoted"):
            attr_name = match.group(1)
            raise AssertionError(f"{attr_name} attribute value must be quoted")

        element = Element.from_match(html, match, "value")

        if element.is_closing:
            attr_name = match.group(1)
            raise AssertionError(f"Invalid use of {attr_name} attribute on closing tag")

        element.value = condition
        elements.append(element)

    elements.sort(key=lambda e: e.tag_start)

    edits: list[AtomicEdit] = []

    for elem in elements:
        if any(other.contains(elem) for other in elements if other is not elem):
            continue

        cleaned_tag = elem.remove_attribute()
        cleaned_tag = re.sub(r"\s*/>$", ">", cleaned_tag)

        replacement = f"{cleaned_tag}{{{{ {elem.value} }}}}{elem.closing_tag()}"

        edits.append(
            AtomicEdit(
                position=elem.tag_start,
                content=replacement,
                is_insert=False,
                end_position=elem.full_end,
            )
        )

    return apply_edits(html, edits)
