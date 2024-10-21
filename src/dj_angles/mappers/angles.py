from typing import TYPE_CHECKING

from django.template import engines
from django.template.exceptions import TemplateDoesNotExist
from minestrone import HTML

from dj_angles.mappers.include import get_include_template_file
from dj_angles.strings import dequotify

if TYPE_CHECKING:
    from dj_angles.tags import Tag


def map_angles_include(tag: "Tag") -> str:
    template_file = dequotify(get_include_template_file(tag))
    wrapping_tag_name = tag.get_wrapping_tag_name(name=template_file)
    template = None

    for engine in engines.all():
        try:
            template = engine.get_template(template_file)

            if template:
                break
        except TemplateDoesNotExist:
            pass

    if template is None:
        return f"<{wrapping_tag_name}>"

    rendered_template = template.render()
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
