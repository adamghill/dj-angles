from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dj_angles.tags import Tag


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

    if not tag.attributes:
        raise AssertionError("{% include %} must have an template name")

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

    if not tag.attributes:
        raise Exception("Missing src")

    src = tag.attributes.pop(0)

    if tag.attributes:
        return f'<img src="{{% static {src} %}}" {tag.attributes} />'

    return f'<img src="{{% static {src} %}}" />'


def map_css(tag: "Tag") -> str:
    """Mapper function for css tags.

    Args:
        param tag: The tag to map.
    """

    if not tag.attributes:
        raise Exception("Missing href")

    href = tag.attributes.pop(0)

    if not tag.attributes.get("rel"):
        tag.attributes.append('rel="stylesheet"')

    return f'<link href="{{% static {href} %}}" {tag.attributes} />'
