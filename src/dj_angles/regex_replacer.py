import re
from collections import deque
from typing import Optional

from django.template import Context, Origin, Template, TemplateDoesNotExist, TemplateSyntaxError
from minestrone import HTML

from dj_angles.exceptions import InvalidEndTagError
from dj_angles.mappers.mapper import get_tag_map
from dj_angles.settings import get_setting, get_tag_regex
from dj_angles.tags import Tag


def _render_template(html: str, origin: Origin):
    # Parse the inner HTML and create a template
    template = Template(html, origin=origin)

    # It would be nice to pass in the template context here, but cannot
    # find access to it with this process, so it is empty
    template.render(context=Context())


def set_tag_inner_html(html, match, tag):
    if (
        not tag.is_self_closing
        and not tag.is_end
        and (tag.django_template_tag is None or tag.is_include or tag.is_error_boundary)
    ):
        match_end_idx = match.end()

        try:
            # Get next ending tag
            # TODO: handle custom tag, not just /dj-
            next_ending_tag_idx = html.index("</dj-", match_end_idx)

            if tag.is_error_boundary:
                # Get next error boundary; they cannot be nested
                next_ending_tag_idx = html.index(f"</dj-{tag.tag_name}>", match_end_idx)

            tag.inner_html = html[match_end_idx:next_ending_tag_idx].strip()
        except ValueError as e:
            raise


def check_for_missing_start_tag(raise_for_missing_start_tag, tag, tag_queue):
    if raise_for_missing_start_tag:
        if tag.is_end:
            last_tag: Tag = tag_queue.pop()

            if last_tag.tag_name != tag.tag_name:
                raise InvalidEndTagError(tag=tag, last_tag=last_tag)
        elif not tag.is_self_closing:
            tag_queue.append(tag)


def get_replacements_for_error_boundaries(tag_regex, origin, tag, replacements):
    matches_to_skip = 0

    if get_setting(key_path="error_boundaries", setting_name="enabled", default=True) is True:
        if tag.is_error_boundary and tag.inner_html:
            matches_to_skip = len(re.findall(tag_regex, tag.inner_html))

            try:
                parsed_inner_html = replace_django_template_tags(tag.inner_html)

                _render_template(parsed_inner_html, origin)

                # # Parse the inner HTML and create a template
                # inner_html_template = Template(parsed_inner_html, origin=origin)

                # # It would be nice to pass in the template context here, but cannot
                # # find access to it with this process, so it is empty
                # inner_html_template.render(context=Context())

                replacements.append((tag.inner_html, parsed_inner_html))
            except (TemplateDoesNotExist, TemplateSyntaxError) as e:
                print("eee", e.__dict__)
                error_html = tag.get_error_html(e)

                replacements.append((tag.inner_html, error_html))

    return matches_to_skip


def get_slots(tag, replacements):
    slots = []

    # Parse the inner HTML for includes to handle slots
    if get_setting("slots_enabled", default=False) and tag.inner_html:
        for element in HTML(tag.inner_html).elements:
            if slot_name := element.attributes.get("slot"):
                slots.append((slot_name, element))

                # Remove slot from the current HTML because it will be injected into the include component
                replacements.append((tag.inner_html, ""))


def get_replacements(
    html: str, *, origin: Origin = None, raise_for_missing_start_tag: bool = True
) -> list[tuple[str, str]]:
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

    map_explicit_tags_only = get_setting("map_explicit_tags_only", default=False)

    matches_to_skip = 0

    for match in re.finditer(tag_regex, html):
        if matches_to_skip > 0:
            matches_to_skip -= 1
            continue

        tag_html = html[match.start() : match.end()].strip()
        tag_name = match.group("tag_name").strip()
        template_tag_args = match.group("template_tag_args").strip()

        if (map_explicit_tags_only or tag_map.get(None) is None) and tag_name.lower() not in tag_map:
            continue

        tag = Tag(
            tag_map=tag_map,
            html=tag_html,
            tag_name=tag_name,
            template_tag_args=template_tag_args,
            tag_queue=tag_queue,
        )

        set_tag_inner_html(html, match, tag)

        check_for_missing_start_tag(raise_for_missing_start_tag, tag, tag_queue)

        matches_to_skip = get_replacements_for_error_boundaries(tag_regex, origin, tag, replacements)

        slots = get_slots(tag, replacements)

        if django_template_tag := tag.get_django_template_tag(slots=slots):
            replacements.append((tag.html, django_template_tag))

    return replacements


def replace_django_template_tags(html: str, origin: Optional[Origin] = None) -> str:
    """Gets a list of replacements based on template HTML, replaces the necessary strings, and returns the new string.

    Args:
        param html: Template HTML.

    Returns:
        The converted template HTML.
    """

    replacements = get_replacements(html=html, origin=origin)

    for r in replacements:
        html = html.replace(
            r[0],
            r[1],
            1,
        )

    return html
