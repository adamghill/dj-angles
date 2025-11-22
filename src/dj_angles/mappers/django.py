import logging
from typing import TYPE_CHECKING

from dj_angles.exceptions import InvalidEndTagError, MissingAttributeError
from dj_angles.strings import dequotify

if TYPE_CHECKING:
    from dj_angles.tags import Tag


logger = logging.getLogger(__name__)


def map_autoescape(tag: "Tag") -> str:
    """Mapper function for autoescape tags.

    Args:
        param tag: The tag to map.
    """

    django_template_tag = tag.tag_name

    if tag.is_end:
        django_template_tag = django_template_tag[0:10]
        django_template_tag = f"end{django_template_tag}"
    else:
        django_template_tag = django_template_tag.replace("-", " ")

    return f"{{% {django_template_tag} %}}"


def map_image(tag: "Tag") -> str:
    """Mapper function for image tags.

    Args:
        param tag: The tag to map.
    """

    src = tag.get_attribute_value_or_first_key("src")

    if tag.attributes:
        return f'<img src="{{% static {src} %}}" {tag.attributes} />'

    return f'<img src="{{% static {src} %}}" />'


def map_css(tag: "Tag") -> str:
    """Mapper function for css tags.

    Args:
        param tag: The tag to map.
    """

    href = tag.get_attribute_value_or_first_key("href")

    if not tag.attributes.get("rel"):
        tag.attributes.append('rel="stylesheet"')

    return f'<link href="{{% static {href} %}}" {tag.attributes} />'


def map_endblock(tag: "Tag", tag_name: str = "block") -> str:
    """Mapper function for endblock tags. Not included in the default mappers and only called by `map_block`.

    Args:
        param tag: The tag to map.
    """

    name = None

    try:
        name = tag.get_attribute_value_or_first_key("name")

        # Check that the end tag name is the same as the start tag's name
        if tag.start_tag:
            tag.start_tag.parse_attributes()

            try:
                start_name = tag.start_tag.get_attribute_value_or_first_key("name")

                if name != start_name:
                    raise InvalidEndTagError(tag, tag.start_tag)
            except MissingAttributeError:
                pass
    except MissingAttributeError:
        pass

    if not name and tag.start_tag:
        # Re-parse start tag attributes since it can empty from the previous parsing
        tag.start_tag.parse_attributes()

        try:
            name = tag.start_tag.get_attribute_value_or_first_key("name")
        except MissingAttributeError:
            pass

    if name:
        # The block tag doesn't actually want/need quoted strings per se, so remove them
        name = dequotify(name)

        return f"{{% end{tag_name} {name} %}}"

    return f"{{% end{tag_name} %}}"


def map_block(tag: "Tag", tag_name: str = "block") -> str:
    """Mapper function for block tags.

    Args:
        param tag: The tag to map.
    """

    if tag.is_end:
        return map_endblock(tag, tag_name)

    if not tag.attributes:
        raise Exception("Missing name")

    name = tag.get_attribute_value_or_first_key("name")

    # The block tag doesn't actually want/need quoted strings per se, so remove them
    name = dequotify(name)

    tag_str = f"{{% {tag_name} {name} "

    # Handle extra attributes which are not needed for the block tag, but are needed
    # for partialdef tags
    if tag.attributes:
        tag_str = f"{tag_str}{tag.attributes} "

    tag_str = f"{tag_str}%}}"

    if tag.is_self_closing:
        return f"{tag_str}{{% end{tag_name} {name} %}}"

    return tag_str


def map_extends(tag: "Tag") -> str:
    """Mapper function for extends tags.

    Args:
        param tag: The tag to map.
    """

    if not tag.attributes:
        raise MissingAttributeError("parent")

    django_template_tag = "extends"

    parent = tag.get_attribute_value_or_first_key("parent")

    if "." not in parent:
        parent = dequotify(parent)
        parent = f"'{parent}.html'"

    return f"{{% {django_template_tag} {parent} %}}"
