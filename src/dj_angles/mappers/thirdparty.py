import logging
from typing import TYPE_CHECKING

from dj_angles.exceptions import MissingAttributeError
from dj_angles.mappers.django import map_block
from dj_angles.strings import dequotify

if TYPE_CHECKING:
    from dj_angles.tags import Tag


logger = logging.getLogger(__name__)


def map_bird(tag: "Tag") -> str:
    """Map `dj-angles` tags to `django-bird` syntax.

    Transforms `<dj-bird name="calendar">` to `{% bird 'calendar' %}`.
    """

    if tag.is_end:
        return "{% endbird %}"

    template_file = tag.tag_name

    if template_file == "bird":
        try:
            template_file = tag.pop_attribute_value_or_first_key("template")
        except MissingAttributeError:
            pass

    django_template_tag = f"{{% bird {template_file}"

    if tag.attributes:
        django_template_tag = f"{django_template_tag} {tag.attributes}"

    if tag.is_self_closing:
        django_template_tag = f"{django_template_tag} /"

    return f"{django_template_tag} %}}"


def map_partial(tag: "Tag") -> str:
    """Map `dj-angles` tags to `django-components` syntax.

    Transforms `<dj-component name="calendar">` to `{% component 'calendar' %}`.
    """

    if tag.is_self_closing:
        name = tag.pop_attribute_value_or_first_key("name")
        name = dequotify(name)

        return f"{{% partial {name} %}}"

    return map_block(tag=tag, tag_name="partialdef")


def map_component(tag: "Tag") -> str:
    """Map `dj-angles` tags to `django-components` syntax.

    Transforms `<dj-component name="calendar">` to `{% component 'calendar' %}`.
    """

    if tag.is_end:
        return "{% endcomponent %}"

    try:
        component_name = tag.pop_attribute_value_or_first_key("name")
    except MissingAttributeError as err:
        raise MissingAttributeError("dj-component requires a 'name' attribute") from err

    component_name = dequotify(component_name)

    django_template_tag = f"{{% component '{component_name}'"

    if tag.attributes:
        django_template_tag = f"{django_template_tag} {tag.attributes}"

    if tag.is_self_closing:
        django_template_tag = f"{django_template_tag} /"

    return f"{django_template_tag} %}}"


def map_viewcomponent(tag: "Tag") -> str:
    """Map `dj-angles` tags to `django-viewcomponent` syntax.

    Transforms `<dj-viewcomponent name="button">` to `{% component 'button' %}{% endcomponent %}`.
    """

    if tag.is_end:
        return "{% endcomponent %}"

    try:
        component_name = tag.pop_attribute_value_or_first_key("name")
    except MissingAttributeError as err:
        raise MissingAttributeError("dj-viewcomponent requires a 'name' attribute") from err

    component_name = dequotify(component_name)

    django_template_tag = f"{{% component '{component_name}'"

    if tag.attributes:
        django_template_tag = f"{django_template_tag} {tag.attributes}"

    django_template_tag = f"{django_template_tag} %}}"

    if tag.is_self_closing:
        return f"{django_template_tag}\n{{% endcomponent %}}"

    return django_template_tag
