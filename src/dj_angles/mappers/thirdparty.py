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


def map_compress(tag: "Tag") -> str:
    """Map `dj-angles` tags to `django-compressor` syntax.

    Syntax: {% compress <js/css> [<file/inline/preload> [block_name]] %}

    Examples:
        - `<dj-compress css>` → `{% compress css %}`
        - `<dj-compress js inline>` → `{% compress js inline %}`
        - `<dj-compress css file name="my-styles">` → `{% compress css file my-styles %}`
    """

    if tag.is_end:
        return "{% endcompress %}"

    # Get the compression type (css or js) from attributes
    compress_type = None

    # Check for 'css' or 'js' as a key-only attribute
    for attr in tag.attributes:
        if attr.key in ("css", "js") and not attr.has_value:
            compress_type = attr.key
            tag.attributes.remove(attr.key)
            break

    # If not found as key-only, check for 'type' attribute
    if compress_type is None:
        try:
            compress_type = tag.pop_attribute_value_or_first_key("type")
            compress_type = dequotify(compress_type)
        except MissingAttributeError:
            compress_type = "css"  # Default to css

    django_template_tag = f"{{% compress {compress_type}"

    # Check for mode: file, inline, or preload (key-only attributes)
    mode = None
    for attr in tag.attributes:
        if attr.key in ("file", "inline", "preload") and not attr.has_value:
            mode = attr.key
            tag.attributes.remove(attr.key)
            break

    if mode:
        django_template_tag = f"{django_template_tag} {mode}"

    # Check for block_name via 'name' attribute
    if name_attr := tag.attributes.get("name"):
        block_name = dequotify(name_attr.value or "")
        tag.attributes.remove("name")
        django_template_tag = f"{django_template_tag} {block_name}"

    return f"{django_template_tag} %}}"
