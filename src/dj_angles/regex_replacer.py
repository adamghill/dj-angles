import re
from collections import deque

from minestrone import HTML

from dj_angles.exceptions import InvalidEndTagError
from dj_angles.mappers.mapper import get_tag_map
from dj_angles.settings import get_setting, get_tag_regex
from dj_angles.strings import replace_newlines
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

    # Handle dj-attributes
    dj_attribute_replacements = []

    for match in re.finditer(r"\s((dj-if|dj-elif)=|dj-else)", html):
        start_idx = match.start()
        value_start_idx = match.end()

        original_html = html
        dj_attribute = (match.groups()[-1] or match.groups()[0]).strip()

        (value, end_idx) = get_end_of_attribute_value(html, value_start_idx)

        new_html = html[:start_idx] + html[end_idx:]

        (tag_name, tag_idx) = get_previous_element_tag(new_html, start_idx)

        end_of_tag_idx = end_of_tag_index(new_html, tag_idx + 1, tag_name)

        conditional_start_tag = ""
        condition_end_tag = ""

        if dj_attribute == "dj-if":
            conditional_start_tag = f"{{% if {value} %}}"
            condition_end_tag = "{% endif %}"
        elif dj_attribute == "dj-elif":
            conditional_start_tag = f"{{% elif {value} %}}"
            condition_end_tag = "{% endif %}"
        elif dj_attribute == "dj-else":
            conditional_start_tag = "{% else %}"
            condition_end_tag = "{% endif %}"
        else:
            raise AssertionError(f"Unknown dj-attribute: {dj_attribute}")

        internal_html = new_html[tag_idx:end_of_tag_idx]

        original_end_of_tag_idx = end_of_tag_index(original_html, tag_idx + 1, tag_name)
        original_internal_html = original_html[tag_idx:original_end_of_tag_idx]

        if dj_attribute in ("dj-elif", "dj-else"):
            if not dj_attribute_replacements:
                raise AssertionError(f"Invalid use of {dj_attribute} outside of a conditional block")

            last_replacement = dj_attribute_replacements.pop(-1)
            original_snippet = last_replacement[0]
            new_snippet = last_replacement[1]

            if dj_attribute == "dj-else":
                if not ("dj-if" in original_snippet or "dj-elif" in original_snippet):
                    raise AssertionError(f"Invalid use of dj-else after: {original_snippet}")
            elif dj_attribute == "dj-elif":
                if "dj-if" not in original_snippet:
                    raise AssertionError(f"Invalid use of dj-elif after: {original_snippet}")

            if new_snippet.endswith("{% endif %}"):
                dj_attribute_replacements.append(
                    (
                        original_snippet,
                        new_snippet[:-11],  # remove the previous {% endif %}
                    ),
                )

        replacement_html = f"{conditional_start_tag}{internal_html}{condition_end_tag}"

        dj_attribute_replacements.append((original_internal_html, replacement_html))

    for r in dj_attribute_replacements:
        html = html.replace(
            r[0],
            r[1],
            1,
        )

    return html


def get_end_of_attribute_value(html: str, start_idx: int) -> (str, int):
    starts_with_double_quote = False
    starts_with_single_quote = False
    idx = 0
    value = ""

    for c in html[start_idx:]:
        if idx == 0 and c == "'":
            starts_with_single_quote = True
            idx += 1
            continue
        elif idx == 0 and c == '"':
            starts_with_double_quote = True
            idx += 1
            continue
        elif starts_with_single_quote and c == "'":
            idx += 1
            break
        elif starts_with_double_quote and c == '"':
            idx += 1
            break
        elif not starts_with_double_quote and not starts_with_single_quote and c == " ":
            break
        elif not starts_with_double_quote and not starts_with_single_quote and c == ">":
            break

        value += c
        idx += 1

    return (value, start_idx + idx)


def get_previous_element_tag(html: str, start_idx: int) -> (str, int):
    start_tag_idx = -1
    tag_name = ""
    inside_single_quote = False
    inside_double_quote = False

    # Start searching backwards from the start_idx, looking for the beginning of a tag
    for i in range(start_idx - 1, -1, -1):
        c = html[i]

        # Toggle the quote flags when encountering quotes
        if c == "'" and not inside_double_quote:
            inside_single_quote = not inside_single_quote
        elif c == '"' and not inside_single_quote:
            inside_double_quote = not inside_double_quote

        # If we find a '<' and we're not inside quotes, we've found the start of a tag
        if c == "<" and not inside_single_quote and not inside_double_quote:
            start_tag_idx = i
            break

    # If we found the start of the tag, extract the tag name
    if start_tag_idx != -1:
        for c in html[start_tag_idx + 1 : start_idx]:  # Start after '<'
            if c in (" ", ">"):
                break

            tag_name += c

    return (tag_name, start_tag_idx)


# List of void elements from: https://www.thoughtco.com/html-singleton-tags-3468620
VOID_ELEMENTS = {
    "area",
    "base",
    "br",
    "col",
    "command",
    "embed",
    "hr",
    "img",
    "input",
    "keygen",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}


def end_of_tag_index(html: str, start_idx: int, tag_name: str) -> int:
    if tag_name in VOID_ELEMENTS:
        idx = html.find("/>", start_idx)

        if idx > -1:
            return idx + 2

        # TOOD: Handle > in attribute strings
        idx = html.find(">", start_idx)

        if idx > -1:
            return idx + 1

    open_tag = f"<{tag_name}"
    close_tag = f"</{tag_name}>"

    depth = 1
    idx = start_idx

    while idx < len(html):
        # Check for opening tag
        if html.startswith(open_tag, idx):
            depth += 1
            idx += len(open_tag)
            continue

        # Check for closing tag
        if html.startswith(close_tag, idx):
            depth -= 1

            if depth == 0:
                return idx + len(close_tag)

        idx += 1

    return -1
