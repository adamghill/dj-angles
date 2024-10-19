import logging
from typing import TYPE_CHECKING

from dj_angles.exceptions import MissingAttributeError
from dj_angles.mappers.utils import get_attribute_value_or_first_key
from dj_angles.strings import dequotify

if TYPE_CHECKING:
    from dj_angles.tags import Tag


logger = logging.getLogger(__name__)


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


def map_image(tag: "Tag") -> str:
    """Mapper function for image tags.

    Args:
        param tag: The tag to map.
    """

    src = get_attribute_value_or_first_key(tag, "src")

    if tag.attributes:
        return f'<img src="{{% static {src} %}}" {tag.attributes} />'

    return f'<img src="{{% static {src} %}}" />'


def map_css(tag: "Tag") -> str:
    """Mapper function for css tags.

    Args:
        param tag: The tag to map.
    """

    href = get_attribute_value_or_first_key(tag, "href")

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

    name = get_attribute_value_or_first_key(tag, "name")

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

    parent = get_attribute_value_or_first_key(tag, "parent")

    if "." not in parent:
        parent = dequotify(parent)
        parent = f"'{parent}.html'"

    return f"{{% {django_template_tag} {parent} %}}"
