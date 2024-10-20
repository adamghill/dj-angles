from typing import TYPE_CHECKING

from dj_angles.exceptions import MissingAttributeError
from dj_angles.mappers.utils import get_attribute_value_or_first_key

if TYPE_CHECKING:
    from dj_angles.tags import Tag


def get_include_template_file(tag: "Tag") -> str:
    try:
        template_file = get_attribute_value_or_first_key(tag, "template")
    except MissingAttributeError:
        template_file = tag.component_name

        if tag.is_end and tag.start_tag:
            tag.start_tag.parse_attributes()
            template_file = get_include_template_file(tag.start_tag)

    is_double_quoted = False

    if template_file.startswith("'") and template_file.endswith("'"):
        template_file = template_file[1:-1]
    elif template_file.startswith('"') and template_file.endswith('"'):
        template_file = template_file[1:-1]
        is_double_quoted = True

    if "." not in template_file:
        template_file = f"{template_file}.html"

    if is_double_quoted:
        template_file = f'"{template_file}"'
    else:
        template_file = f"'{template_file}'"

    return template_file


def map_include(tag: "Tag") -> str:
    """Mapper function for include tags.

    Args:
        param tag: The tag to map.
    """

    if not tag.attributes and not tag.is_end:
        raise AssertionError("{% include %} must have an template name")

    template_file = get_include_template_file(tag)

    wrapping_tag_name = tag.get_wrapping_tag_name(name=template_file)

    if tag.is_end:
        return f"</{wrapping_tag_name}>"

    if ":" in template_file:
        colon_idx = template_file.index(":")
        extension_idx = template_file.index(".")
        template_file = template_file[0:colon_idx] + template_file[extension_idx:]

    replacement = ""

    if tag.attributes:
        replacement = f"{{% include {template_file} {tag.attributes} %}}"
    else:
        replacement = f"{{% include {template_file} %}}"

    if tag.is_shadow:
        replacement = f"<template shadowrootmode='open'>{replacement}"

        if tag.is_self_closing:
            replacement = f"{replacement}</template>"

    replacement = f"<{wrapping_tag_name}>{replacement}"

    if tag.is_self_closing:
        replacement = f"{replacement}</{wrapping_tag_name}>"

    return replacement
