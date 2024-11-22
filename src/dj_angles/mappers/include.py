from typing import TYPE_CHECKING

<<<<<<< HEAD
from django.template import TemplateDoesNotExist, TemplateSyntaxError

from dj_angles.exceptions import InvalidAttributeError, MissingAttributeError
from dj_angles.settings import get_setting
from dj_angles.strings import dequotify
=======
from dj_angles.exceptions import MissingAttributeError
>>>>>>> b8109bf (Remove support for boundary from includes, add new tag and add support to blocks.)
from dj_angles.templates import get_template

if TYPE_CHECKING:
    from dj_angles.tags import Tag


def get_include_template_file(tag: "Tag") -> str:
    """Get the template file based for include-like tags.

    Tries to use a template attribute, but falls back to `Tag.tag_name`. Also attempts to handle
    retrieving the correct ending tag based on the start tag (if possible).
    """

    try:
        template_file = None

        try:
            template_file = tag.pop_attribute_value_or_first_key("src")
        except MissingAttributeError:
            # Re-parse attributes in case the previous call popped off an attribute
            tag.parse_attributes()

        if not template_file:
            template_file = tag.pop_attribute_value_or_first_key("template")
    except MissingAttributeError:
        template_file = tag.tag_name

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
        if tag.is_wrapped:
            return f"</{wrapping_tag_name}>"

        return ""

    if ":" in template_file:
        colon_idx = template_file.index(":")
        extension_idx = template_file.index(".")
        template_file = template_file[0:colon_idx] + template_file[extension_idx:]

    if template := get_template(template_file, raise_exception=False):
        template_file = f"'{template.template.name}'"

    replacement = ""

    # Remove the `class` attribute (and store it for later) if it's there
    if wrapper_classes := tag.attributes.pop_value("class") or "":
        if dequotify(wrapper_classes) and not tag.is_wrapped:
            raise InvalidAttributeError(
                name=tag.tag_name, message="`no-wrap` and `class` attributes cannot be used together"
            )

        wrapper_classes = f" class={wrapper_classes}"

    # Remove the `no-wrap` attribute if it's there
    if not tag.is_wrapped:
        tag.attributes.remove("no-wrap")

    if tag.attributes:
        replacement = f"{{% include {template_file} {tag.attributes} %}}"
    else:
        replacement = f"{{% include {template_file} %}}"

    if tag.is_shadow:
        replacement = f"<template shadowrootmode='open'>{replacement}"

        if tag.is_self_closing:
            replacement = f"{replacement}</template>"

    if tag.is_wrapped:
        replacement = f"<{wrapping_tag_name}{wrapper_classes}>{replacement}"

        if tag.is_self_closing:
            replacement = f"{replacement}</{wrapping_tag_name}>"

    return replacement
