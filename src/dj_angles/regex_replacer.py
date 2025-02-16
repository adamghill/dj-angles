import logging
import re
from collections import deque
from dataclasses import dataclass

from minestrone import HTML

from dj_angles.exceptions import InvalidEndTagError
from dj_angles.htmls import find_character, get_outer_html
from dj_angles.mappers.mapper import get_tag_map
from dj_angles.settings import get_setting, get_tag_regex
from dj_angles.strings import dequotify, replace_newlines
from dj_angles.tags import Tag

logger = logging.getLogger(__name__)


@dataclass
class Replacement:
    original: str
    replacement: str
    tag: Tag
    keep_endif: bool = False
    tag_start_idx: int = -1

    def __repr__(self):
        return f"Replacement(original={self.original!r}, replacement={self.replacement!r})"


def get_tag_replacements(html: str, *, raise_for_missing_start_tag: bool = True) -> list[Replacement]:
    """Get a list of tag replacements based on the template HTML.

    Args:
        param html: Template HTML.
        param raise_for_missing_start_tag: Whether or not to raise an error if an invalid tag is discovered.

    Returns:
        A list of tuples where the first item in the tuple is the existing tag element, e.g. "<dj-csrf />"
        and the second item is the replacement string, e.g. "{% csrf_token %}".
    """

    replacements: list[Replacement] = []
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

            try:
                # TODO: handle custom tag, not just /dj-
                next_ending_tag_idx = html.index("</dj-", end_of_include_tag)
                inner_html = html[end_of_include_tag:next_ending_tag_idx].strip()

                if inner_html:
                    for element in HTML(inner_html).elements:
                        if slot_name := element.attributes.get("slot"):
                            slots.append((slot_name, element))

                            # Remove slot from the current HTML because it will be injected into the include component
                            replacements.append(Replacement(original=inner_html, replacement="", tag=tag))
            except ValueError:
                # Ending tag could not be found, so skip getting the inner html
                pass

        django_template_tag = tag.get_django_template_tag(slots=slots)

        if django_template_tag:
            replacements.append(Replacement(original=tag.html, replacement=django_template_tag, tag=tag))

    return replacements


def get_attribute_replacements(html: str) -> list[Replacement]:
    """Get a list of attribute replacements based on the template HTML.

    Args:
        param html: Template HTML.

    Returns:
        A list of `Replacement` where `original` is the existing element, e.g. "<div dj-if="True"></div>"
        and `replacement` is the replacement string, e.g. "{% if True %}<div></div>{% endif %}".
    """

    replacements: list[Replacement] = []

    initial_attribute_regex = get_setting("initial_attribute_regex", default=r"(dj-)")
    if_attribute_regex = re.compile(rf"{initial_attribute_regex}if")
    elif_attribute_regex = re.compile(rf"{initial_attribute_regex}elif")
    else_attribute_regex = re.compile(rf"{initial_attribute_regex}else")
    endif_attribute_regex = re.compile(rf"({initial_attribute_regex}endif|{initial_attribute_regex}fi)")

    for match in re.finditer(
        rf"\s(({initial_attribute_regex}if|{initial_attribute_regex}elif)=|{initial_attribute_regex}else|{initial_attribute_regex}endif|{initial_attribute_regex}fi)",
        html,
    ):
        dj_attribute = (match.groups()[1] or match.groups()[0]).strip()

        attribute_start_idx = match.start()

        value_start_idx = match.end()
        value_end_idx = find_character(html, value_start_idx, character_regex=r"[\s>]")
        value = html[value_start_idx:value_end_idx]
        value = dequotify(value)

        conditional_start_tag = ""
        condition_end_tag = ""
        is_explicit_endif = False
        is_implicit_endif = False

        if if_attribute_regex.search(dj_attribute):
            conditional_start_tag = f"{{% if {value} %}}"
            condition_end_tag = "{% endif %}"
        elif elif_attribute_regex.search(dj_attribute):
            conditional_start_tag = f"{{% elif {value} %}}"
            condition_end_tag = "{% endif %}"
        elif else_attribute_regex.search(dj_attribute):
            conditional_start_tag = "{% else %}"
            condition_end_tag = "{% endif %}"
        elif endif_attribute_regex.search(dj_attribute):
            pass
        else:
            raise AssertionError(f"Unknown attribute: {dj_attribute}")

        # Get the outer HTML of the tag that the attribute is in
        tag_start_idx = find_character(html, value_start_idx, "<", reverse=True)
        tag = get_outer_html(html, tag_start_idx)

        if not tag:
            raise AssertionError("Tag could not be found")

        if tag.is_end and endif_attribute_regex.search(tag.html):
            # Remove the explicit endif from the end tag and mark it and the previous tag as having an explicit endif
            replacement_idx = len(replacements) - 1

            while replacement_idx >= 0:
                previous_replacement = replacements[replacement_idx]

                if previous_replacement.replacement.endswith("{% endif %}"):
                    previous_replacement.replacement = previous_replacement.replacement[:-11]

                if if_attribute_regex.search(previous_replacement.original):
                    break

                replacement_idx -= 1

            replacement_html = endif_attribute_regex.sub("", tag.html).replace(" >", ">") + "{% endif %}"

            new_replacement = Replacement(
                original=tag.html,
                replacement=replacement_html,
                tag=tag,
                keep_endif=True,
                tag_start_idx=tag_start_idx,
            )

            replacements.append(new_replacement)
            continue

        if replacements:
            previous_replacement = replacements[-1]

            if previous_replacement.tag_start_idx > -1:
                if tag_start_idx > previous_replacement.tag_start_idx:
                    if tag_start_idx < len(previous_replacement.tag.outer_html) + previous_replacement.tag_start_idx:
                        is_implicit_endif = True
                        # is_explicit_endif = True

        # Remove the dj_angles attribute from the tag's HTML
        replacement_html = (
            tag.outer_html[: attribute_start_idx - tag_start_idx] + tag.outer_html[value_end_idx - tag_start_idx :]
        )

        if elif_attribute_regex.search(dj_attribute) or else_attribute_regex.search(dj_attribute):
            # Check that dj-elif and dj-else attributes are used in a conditional block
            if not replacements:
                raise AssertionError(f"Invalid use of {dj_attribute} outside of a conditional block")

            replacement_idx = len(replacements) - 1

            while replacement_idx >= 0:
                previous_replacement = replacements[replacement_idx]

                if not previous_replacement.keep_endif:
                    if else_attribute_regex.search(dj_attribute):
                        if not (
                            elif_attribute_regex.search(previous_replacement.original)
                            or if_attribute_regex.search(previous_replacement.original)
                        ):
                            raise AssertionError(f"Invalid use of {dj_attribute} attribute")
                    elif elif_attribute_regex.search(dj_attribute):
                        if not (
                            if_attribute_regex.search(previous_replacement.original)
                            or elif_attribute_regex.search(previous_replacement.original)
                        ):
                            raise AssertionError(f"Invalid use of {dj_attribute} attribute")

                    # Remove {% endif %} from the previous replacement
                    if previous_replacement.replacement.endswith("{% endif %}"):
                        replacements[replacement_idx].original = previous_replacement.original
                        replacements[replacement_idx].replacement = previous_replacement.replacement[:-11]
                        replacements[replacement_idx].tag = previous_replacement.tag
                        replacements[replacement_idx].keep_endif = is_explicit_endif
                        replacements[replacement_idx].tag_start_idx = previous_replacement.tag_start_idx

                        break

                replacement_idx -= 1

        replacement_html = f"{conditional_start_tag}{replacement_html}{condition_end_tag}"
        new_replacement = Replacement(
            original=tag.outer_html,
            replacement=replacement_html,
            tag=tag,
            keep_endif=is_explicit_endif or is_implicit_endif,
            tag_start_idx=tag_start_idx,
        )
        replacements.append(new_replacement)

    # print()
    # for r in replacements:
    #     print(r)
    # print()

    logger.debug("Attribute replacements: %s", replacements)

    return replacements


def convert_template(html: str) -> str:
    """Gets a list of replacements based on template HTML, replaces the necessary strings, and returns the new string.

    Args:
        param html: Template HTML.

    Returns:
        The converted template HTML.
    """

    # Replace dj-angles attributes first
    for replacement in get_attribute_replacements(html=html):
        html = html.replace(
            replacement.original,
            replacement.replacement,
            1,
        )

    # Replace dj_angles tags
    for replacement in get_tag_replacements(html=html):
        html = html.replace(
            replacement.original,
            replacement.replacement,
            1,
        )

    return html
