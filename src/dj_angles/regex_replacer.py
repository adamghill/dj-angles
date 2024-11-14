import re
from collections import deque

from minestrone import HTML

from dj_angles.exceptions import InvalidEndTagError
from dj_angles.mappers.mapper import get_tag_map
from dj_angles.settings import get_setting, get_tag_regex
from dj_angles.tags import Tag


def get_replacements(html: str, *, raise_for_missing_start_tag: bool = True) -> list[tuple[str, str]]:
    """Get a list of replacements (tuples that consists of 2 strings) based on the template HTML.

    Args:
        param html: Template HTML.
        param raise_for_missing_start_tag: Whether or not to raise an error if an invalid tag is discovered.

    Returns:
        A list of tuples where the first item in the tuple is the existing tag element, e.g. "<dj-csrf />"
        and the second item is the replacement string, e.g. "{% csrf_token %}".
    """

    replacements = []
    tag_regex = get_tag_regex()
    tag_queue: deque = deque()

    tag_map = get_tag_map()

    for match in re.finditer(tag_regex, html):
        tag_html = html[match.start() : match.end()].strip()
        tag_name = match.group("tag_name").strip()
        template_tag_args = match.group("template_tag_args").strip()

        tag = Tag(
            tag_map=tag_map,
            html=tag_html,
            tag_name=tag_name,
            template_tag_args=template_tag_args,
            tag_queue=tag_queue,
        )

        if raise_for_missing_start_tag:
            if tag.is_end:
                last_tag: Tag = tag_queue.pop()

                if last_tag.tag_name != tag.tag_name:
                    raise InvalidEndTagError(tag=tag, last_tag=last_tag)
            elif not tag.is_self_closing:
                tag_queue.append(tag)

        slots = []

        # Parse the inner HTML for includes to handle slots
        if (
            get_setting("slots_enabled", default=False)
            and not tag.is_self_closing
            and not tag.is_end
            and (tag.django_template_tag is None or tag.is_include)
        ):
            end_of_include_tag = match.end()

            try:
                # TODO: handle custom tag, not just /dj-
                next_ending_tag_idx = html.index("</dj-", end_of_include_tag)
                inner_html = html[end_of_include_tag:next_ending_tag_idx].strip()

                if inner_html:
                    for element in HTML(inner_html).elements:
                        if slot_name := element.attributes.get("slot"):
                            slots.append((slot_name, element))

                            # Remove slot from the current HTML because it will be injected into the include component
                            replacements.append((inner_html, ""))
            except ValueError:
                # Ending tag could not be found, so skip getting the inner html
                pass

        django_template_tag = tag.get_django_template_tag(slots=slots)

        if django_template_tag:
            replacements.append((tag.html, django_template_tag))

    return replacements


def replace_django_template_tags(html: str) -> str:
    """Gets a list of replacements based on template HTML, replaces the necessary strings, and returns the new string.

    Args:
        param html: Template HTML.

    Returns:
        The converted template HTML.
    """

    replacements = get_replacements(html=html)

    for r in replacements:
        html = html.replace(
            r[0],
            r[1],
            1,
        )

    return html
