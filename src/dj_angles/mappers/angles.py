from typing import TYPE_CHECKING

from minestrone import HTML

from dj_angles.mappers.include import get_include_template_file, map_include
from dj_angles.strings import dequotify
from dj_angles.templates import get_template

if TYPE_CHECKING:
    from dj_angles.tags import Tag


def default_mapper(tag: "Tag") -> str:
    """The default mapper which gets used when no other mapper matches a key in the `tag_map`.

    Basically works like `map_include` except the element's name is used for the template file.

    Examples:
        - `<dj-partial />` is equivalent to `<dj-include 'partial' />`

    Args:
        param tag: The tag to map.
    """

    # Assume the tag name should be the first attribute (as expected for includes)
    tag.attributes.prepend(tag.tag_name)

    django_template_tag = map_include(tag)

    if (tag.is_end and tag.is_shadow) or (tag.start_tag and tag.start_tag.is_shadow):
        django_template_tag = f"</template>{django_template_tag}"

    return django_template_tag


def map_angles_include(tag: "Tag") -> str:
    """Mapper function for the angles include tag; handles the implementation of slots.

    Args:
        param tag: The tag to map.
    """

    template_file = dequotify(get_include_template_file(tag))
    wrapping_tag_name = tag.get_wrapping_tag_name(name=template_file)
    template = get_template(template_file)

    if template is None:
        return f"<{wrapping_tag_name}>"

    rendered_template = str(template.render())
    html = HTML(rendered_template)

    for element in html.query("slot"):
        slot_name = element.attributes.get("name")

        for slots_slot_name, slot_element in tag.slots:
            if slot_name == slots_slot_name:
                element.remove_children()
                element.insert(slot_element)

    rendered_template = str(html)

    # Prepend the wrapping tag name on to the template; the end tag happens later
    rendered_template = f"<{wrapping_tag_name}>{rendered_template}"

    return rendered_template


def map_call(tag: "Tag", template_tag_name: str = "call") -> str:
    """Mapper function for the dj-angles call template tag.

    Args:
        param tag: The tag to map.
        param template_tag_name: The name of the template tag to use. Defaults to "call".
    """

    if tag.is_end:
        return ""

    code = dequotify(tag.get_attribute_value_or_first_key("code"))
    context_template_variable_attr = tag.attributes.get("as")

    if context_template_variable_attr is not None:
        if hasattr(context_template_variable_attr, "value") and context_template_variable_attr.value:
            context_template_variable = dequotify(context_template_variable_attr.value)

            return f"{{% {template_tag_name} {code} as {context_template_variable} %}}"

    return f"{{% {template_tag_name} {code} %}}"


def map_model(tag: "Tag") -> str:
    """Mapper function for the dj-angles model template tag.

    Args:
        param tag: The tag to map.
    """

    return map_call(tag, template_tag_name="model")


def map_form(tag: "Tag") -> str:
    """Mapper function for the dj-angles form template tag.

    Args:
        param tag: The tag to map.
    """

    # TODO: support url, reverse, etc?

    if tag.is_end:
        if tag.start_tag and tag.start_tag.attributes.has("ajax"):
            return "</ajax-form></form>"

        return "</form>"

    swap = tag.attributes.pluck_value("swap") or "'outerHTML'"
    delay = tag.attributes.pluck_value("delay") or 0

    if is_csrf := tag.attributes.has("csrf"):
        tag.attributes.remove("csrf")

    if is_ajax := tag.attributes.has("ajax"):
        tag.attributes.remove("ajax")

    html = f"<form {tag.attributes}>"

    if is_ajax:
        html = f"<ajax-form swap={swap} delay='{delay}'>{html}"

    if is_csrf:
        html = f"{html}{{% csrf_token %}}"

    return html
