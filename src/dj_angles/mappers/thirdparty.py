import logging
from typing import TYPE_CHECKING

from dj_angles.exceptions import MissingAttributeError
from dj_angles.mappers.django import map_block

if TYPE_CHECKING:
    from dj_angles.tags import Tag


logger = logging.getLogger(__name__)


def map_bird(tag: "Tag") -> str:
    if tag.is_end:
        return "{% endbird %}"

    template_file = tag.tag_name

    if template_file == "bird":
        try:
            template_file = tag.get_attribute_value_or_first_key("template")
        except MissingAttributeError:
            pass

    django_template_tag = f"{{% bird {template_file}"

    if tag.attributes:
        django_template_tag = f"{django_template_tag} {tag.attributes}"

    if tag.is_self_closing:
        django_template_tag = f"{django_template_tag} /"

    return f"{django_template_tag} %}}"


def map_partialdef(tag: "Tag") -> str:
    return map_block(tag=tag, tag_name="partialdef")
