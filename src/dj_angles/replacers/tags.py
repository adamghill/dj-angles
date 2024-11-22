import logging
import re
from collections import deque
from typing import Optional

from django.template import Context, Origin, Template, TemplateDoesNotExist, TemplateSyntaxError
from minestrone import HTML

from dj_angles.exceptions import InvalidEndTagError
from dj_angles.mappers.mapper import get_tag_map
from dj_angles.replacers.objects import AtomicEdit, apply_edits
from dj_angles.settings import get_setting, get_tag_regex
from dj_angles.strings import replace_newlines
from dj_angles.tags import Tag

logger = logging.getLogger(__name__)


def replace_tags(html: str, *, origin: Optional[Origin] = None, raise_for_missing_start_tag: bool = True) -> str:
    """Get a list of tag replacements based on the template HTML.

    Args:
        html: Template HTML.
        origin: The origin of the template.
        raise_for_missing_start_tag: Whether or not to raise an error if an invalid tag is discovered.

    Returns:
        The converted template HTML.
    """

    edits: list[AtomicEdit] = []
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
        template_tag_args = replace_newlines(template_tag_args, " ")

        if (map_explicit_tags_only or tag_map.get(None) is None) and tag_name.lower() not in tag_map:
            continue

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

        # Parse the inner HTML for includes to handle slots or error boundaries
        if (
            not tag.is_self_closing
            and not tag.is_end
            and (
                (get_setting("slots_enabled", default=False) and (tag.django_template_tag is None or tag.is_include))
                or getattr(tag, "is_error_boundary", False)
            )
        ):
            end_of_include_tag = match.end()

            # Find the next closing tag
            if getattr(tag, "is_error_boundary", False):
                closing_tag_pattern = rf"</{tag.tag_name}"
            else:
                initial_tag_regex = get_setting("initial_tag_regex", default=r"(dj-)")
                closing_tag_pattern = rf"</{initial_tag_regex}"

            closing_match = re.search(closing_tag_pattern, html[end_of_include_tag:])

            if closing_match:
                inner_html = html[end_of_include_tag : end_of_include_tag + closing_match.start()].strip()

                if inner_html:
                    # Capture the start and end of the inner content relative to the full HTML
                    # We need to find the position of the stripped content within the raw content
                    # to preserve surrounding whitespace (like newlines) which the original implementation did.
                    raw_inner_range_start = end_of_include_tag
                    raw_inner_range_end = end_of_include_tag + closing_match.start()
                    raw_inner = html[raw_inner_range_start:raw_inner_range_end]

                    # Calculate offsets for stripped content
                    leading_whitespace_len = len(raw_inner) - len(raw_inner.lstrip())
                    trailing_whitespace_len = len(raw_inner) - len(raw_inner.rstrip())

                    inner_start_pos = raw_inner_range_start + leading_whitespace_len
                    inner_end_pos = raw_inner_range_end - trailing_whitespace_len

                    if getattr(tag, "is_error_boundary", False):
                        # Skip processing the inner tags in the main loop since we are handling them recursively/here
                        matches_to_skip = len(re.findall(tag_regex, raw_inner))

                        try:
                            parsed_inner_html = replace_tags(
                                inner_html, origin=origin, raise_for_missing_start_tag=raise_for_missing_start_tag
                            )

                            # Parse the inner HTML and create a template to check for syntax errors
                            inner_html_template = Template(parsed_inner_html, origin=origin)

                            # It would be nice to pass in the template context here, but cannot
                            # find access to it with this process, so it is empty
                            inner_html_template.render(context=Context())

                            replacements_content = parsed_inner_html
                        except (TemplateDoesNotExist, TemplateSyntaxError) as e:
                            replacements_content = tag.get_error_html(e)

                        edits.append(
                            AtomicEdit(
                                position=inner_start_pos,
                                content=replacements_content,
                                is_insert=False,
                                end_position=inner_end_pos,
                            )
                        )
                    else:
                        # Slots logic
                        found_slot = False
                        for element in HTML(inner_html).elements:
                            if slot_name := element.attributes.get("slot"):
                                slots.append((slot_name, element))
                                found_slot = True

                        if found_slot:
                            # Remove slot content from the current HTML because it will be injected into the include
                            # component; use calculated inner_start_pos and inner_end_pos to precisely target the
                            # stripped content
                            edits.append(
                                AtomicEdit(
                                    position=inner_start_pos, content="", is_insert=False, end_position=inner_end_pos
                                )
                            )

        django_template_tag = tag.get_django_template_tag(slots=slots)

        if django_template_tag:
            edits.append(
                AtomicEdit(
                    position=match.start(), content=django_template_tag, is_insert=False, end_position=match.end()
                )
            )

    return apply_edits(html, edits)
