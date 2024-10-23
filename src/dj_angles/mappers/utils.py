from typing import TYPE_CHECKING

from dj_angles.exceptions import MissingAttributeError

if TYPE_CHECKING:
    from dj_angles.tags import Tag


def get_attribute_value_or_first_key(tag: "Tag", attribute_name: str) -> str:
    """Gets the first attribute key or the first value for a particular attribute name.

    Args:
        param tag: The tag to get attributes from.
        param attribute_name: The name of the attribute to get.
    """

    attr = tag.attributes.get(attribute_name)

    if attr:
        tag.attributes.remove(attribute_name)

        return attr.value or ""

    try:
        attr = tag.attributes.pop(0)
    except IndexError as err:
        raise MissingAttributeError(attribute_name) from err

    val = None

    if not attr.has_value:
        val = attr.key

    if not val:
        raise MissingAttributeError(attribute_name)

    return val
