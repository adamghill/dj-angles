import logging
import re
from collections import deque

from minestrone import HTML

from dj_angles.exceptions import InvalidEndTagError
from dj_angles.mappers.mapper import get_tag_map
from dj_angles.replacers.objects import AtomicEdit, apply_edits
from dj_angles.settings import get_setting, get_tag_regex
from dj_angles.strings import replace_newlines
from dj_angles.tags import Tag

logger = logging.getLogger(__name__)


def replace_tags(html: str, *, raise_for_missing_start_tag: bool = True) -> str:
    """Get a list of tag replacements based on the template HTML.

    Args:
        html: Template HTML.
        raise_for_missing_start_tag: Whether or not to raise an error if an invalid tag is discovered.

    Returns:
        The converted template HTML.
    """

    edits: list[AtomicEdit] = []
    tag_regex = get_tag_regex()
    tag_queue: deque = deque()
    tag_map = get_tag_map()

    map_explicit_tags_only = get_setting("map_explicit_tags_only", False)

    for match in re.finditer(tag_regex, html):
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

        # Parse the inner HTML for includes to handle slots
        if (
            get_setting("slots_enabled", default=False)
            and not tag.is_self_closing
            and not tag.is_end
            and (tag.django_template_tag is None or tag.is_include)
        ):
            end_of_include_tag = match.end()

            # Find the next closing tag that matches the initial_tag_regex setting
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

                    found_slot = False
                    for element in HTML(inner_html).elements:
                        if slot_name := element.attributes.get("slot"):
                            slots.append((slot_name, element))
                            found_slot = True

                    if found_slot:
                        # Remove slot content from the current HTML because it will be injected into the include component
                        # We use calculated inner_start_pos and inner_end_pos to precisely target the stripped content
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
