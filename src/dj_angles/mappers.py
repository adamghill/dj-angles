import logging
from typing import TYPE_CHECKING

from dj_angles.exceptions import MissingAttributeError
from dj_angles.strings import dequotify

if TYPE_CHECKING:
    from dj_angles.tags import Tag


logger = logging.getLogger(__name__)


def _get_attribute_value_or_first_key(tag: "Tag", attribute_name: str) -> str:
    """Gets the first attribute key or the first value for a particular attribute name.

    Args:
        param tag: The tag to get attributes from.
        param attribute_name: The name of the attribute to get.
    """

    attr = tag.attributes.get(attribute_name)

    if attr:
        tag.attributes.remove(attribute_name)
        return attr.value

    attr = tag.attributes.pop(0)
    val = None

    if not attr.has_value:
        val = attr.key

    if not val:
        raise MissingAttributeError(attribute_name)

    return val


def map_autoescape(tag: "Tag") -> str:
    """Mapper function for autoescape tags.

    Args:
        param tag: The tag to map.
    """

    django_template_tag = tag.component_name

    if tag.is_end:
        django_template_tag = django_template_tag[0:10]
        django_template_tag = f"end{django_template_tag}"
    else:
        django_template_tag = django_template_tag.replace("-", " ")

    return f"{{% {django_template_tag} %}}"


def map_include(tag: "Tag") -> str:
    """Mapper function for include tags.

    Args:
        param tag: The tag to map.
    """

    if tag.is_end:
        return ""

    if not tag.attributes:
        raise AssertionError("{% include %} must have an template name")

    template_file = ""
    template_attr = tag.attributes.get("template")

    if template_attr:
        tag.attributes.remove(template_attr.key)
        template_file = template_attr.value
    else:
        first_attribute = tag.attributes.pop(0)
        template_file = first_attribute.key

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

    wrapping_tag_name = tag.get_wrapping_tag_name(name=template_file)

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
        replacement = f"<{wrapping_tag_name}><template shadowrootmode='open'>{replacement}"

        if tag.is_self_closing:
            replacement = f"{replacement}</template></{wrapping_tag_name}>"
    else:
        replacement = f"<{wrapping_tag_name}>{replacement}"

        if tag.is_self_closing:
            replacement = f"{replacement}</{wrapping_tag_name}>"

    return replacement


def map_image(tag: "Tag") -> str:
    """Mapper function for image tags.

    Args:
        param tag: The tag to map.
    """

    src = _get_attribute_value_or_first_key(tag, "src")

    if tag.attributes:
        return f'<img src="{{% static {src} %}}" {tag.attributes} />'

    return f'<img src="{{% static {src} %}}" />'


def map_css(tag: "Tag") -> str:
    """Mapper function for css tags.

    Args:
        param tag: The tag to map.
    """

    href = _get_attribute_value_or_first_key(tag, "href")

    if not tag.attributes.get("rel"):
        tag.attributes.append('rel="stylesheet"')

    return f'<link href="{{% static {href} %}}" {tag.attributes} />'


def map_block(tag: "Tag") -> str:
    """Mapper function for block tags.

    Args:
        param tag: The tag to map.
    """

    if not tag.attributes:
        raise Exception("Missing block name")

    django_template_tag = "block"

    if tag.is_end:
        django_template_tag = "endblock"

    name = _get_attribute_value_or_first_key(tag, "name")

    # The block tag doesn't actually want/need quoted strings per se, so remove them
    name = dequotify(name)

    return f"{{% {django_template_tag} {name} %}}"


def map_extends(tag: "Tag") -> str:
    """Mapper function for extends tags.

    Args:
        param tag: The tag to map.
    """

    if not tag.attributes:
        raise MissingAttributeError("parent")

    django_template_tag = "extends"

    parent = _get_attribute_value_or_first_key(tag, "parent")

    return f"{{% {django_template_tag} {parent} %}}"
