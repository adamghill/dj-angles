from typing import TYPE_CHECKING

from django.template import TemplateDoesNotExist, TemplateSyntaxError

from dj_angles.exceptions import MissingAttributeError
from dj_angles.settings import get_setting
from dj_angles.strings import dequotify
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
            template_file = tag.get_attribute_value_or_first_key("src")
        except MissingAttributeError:
            # Re-parse attributes in case the previous call popped off an attribute
            tag.parse_attributes()

        if not template_file:
            template_file = tag.get_attribute_value_or_first_key("template")
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
        return f"</{wrapping_tag_name}>"

    if ":" in template_file:
        colon_idx = template_file.index(":")
        extension_idx = template_file.index(".")
        template_file = template_file[0:colon_idx] + template_file[extension_idx:]

    try:
        # By default do not raise exceptions for invalid templates if running unit tests
        raise_on_invalid_template = not get_setting("IS_IN_UNIT_TEST", default=False)

        if template := get_template(template_file, raise_exception=raise_on_invalid_template):
            template.render()

            template_file = f"'{template.template.name}'"
    except (TemplateDoesNotExist, TemplateSyntaxError) as e:
        handle_errors = (
            get_setting(key_path="error_boundaries", setting_name="enabled", default=True) is True
            or tag.error_boundary is True
        )

        if handle_errors:
            error_html = ""
            template_file = dequotify(template_file)

            if hasattr(e, "template_debug"):
                error_html = (
                    f"Error parsing {template_file}: {e} in {e.template_debug['name']} line {e.template_debug['line']}"
                )
            elif hasattr(e, "tried"):
                if e.tried:
                    error_html = f"<h1>{template_file}</h1><p>Tried: {', '.join(e.tried) or 'Unknown'}</p>"
                else:
                    error_html = f"<h1>{template_file}</h1><p>{e}</p>"
            else:
                error_html = "<h1>{template_file}</h1><p>{e}</p>"

            if get_setting(key_path="error_boundaries", setting_name="shadow", default=True):
                return tag.get_error(f"<template shadowrootmode='open'>{error_html}</template>")

            return tag.get_error(error_html)

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
