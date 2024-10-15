import logging
from typing import TYPE_CHECKING

from dj_angles.mappers.utils import get_attribute_value_or_first_key

if TYPE_CHECKING:
    from dj_angles.tags import Tag


logger = logging.getLogger(__name__)


def map_bird(tag: "Tag") -> str:
    if tag.is_end:
        return "{% endbird %}"

    template = get_attribute_value_or_first_key(tag, "template")
    django_template_tag = f"{{% bird {template}"

    if tag.attributes:
        django_template_tag = f"{django_template_tag} {tag.attributes}"

    if tag.is_self_closing:
        django_template_tag = f"{django_template_tag} /"

    return f"{django_template_tag} %}}"
