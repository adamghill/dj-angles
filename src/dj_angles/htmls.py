import re

from dj_angles.tags import Tag

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


def get_outer_html(html: str, start_idx: int) -> Tag | None:
    """Get the outer HTML for just the tag at a given index.

    Will not return HTML before the beginning of the tag or after the ending tag.

    Example:
        >>> tag = get_outer_html("<span></span><div dj-if='True'><p>test</p></div><span></span>", 14)
        >>> tag.outer_html
        "<div dj-if='True'><p>test</p></div>"

    Args:
        html (str): The HTML string to search.
        start_idx (int, optional): The index to start searching from.

    Returns:
        Tag: The tag at the given index. The outer HTML is set on `tag.outer_html`.
    """

    initial_tag: Tag | None = None
    idx = start_idx
    tag_html = ""
    tag_name = ""

    in_double_quote = False
    in_single_quote = False

    while range(start_idx, len(html)):
        if idx >= len(html):
            break

        c = html[idx]

        # Skip text that aren't tags, e.g. inner text
        if not tag_html and c != "<":
            idx += 1
            continue

        tag_html += c

        if not tag_name and c == " ":
            tag_name = tag_html[1:].strip()
        elif c == '"':
            in_double_quote = not in_double_quote
        elif c == "'":
            in_single_quote = not in_single_quote
        elif not in_double_quote and not in_single_quote and c == ">":
            if not tag_name:
                tag_name = tag_html[1:-1].strip()

            if tag_name.startswith("/"):
                tag_name = tag_name[1:]

            tag = Tag(html=tag_html, tag_name=tag_name)

            if not initial_tag:
                if tag.is_self_closing:
                    tag.outer_html = tag_html

                    return tag

                initial_tag = tag
            elif initial_tag and initial_tag.tag_name == tag.tag_name:
                if tag.is_end:
                    end_of_tag_idx = idx + 1
                    initial_tag.outer_html = html[start_idx:end_of_tag_idx]

                    return initial_tag

            tag_html = ""
            tag_name = ""

        idx += 1

    if initial_tag and (initial_tag.can_be_void or initial_tag.is_end):
        initial_tag.outer_html = initial_tag.html

        return initial_tag

    return None


def find_character(
    html: str,
    start_idx: int,
    character: str | None = None,
    character_regex: str | None = None,
    *,
    reverse: bool = False,
) -> int:
    if character is None and character_regex is None:
        raise ValueError("Either character or character_regex must be provided")

    character_regex_re = None
    if character_regex is not None:
        character_regex_re = re.compile(character_regex)

    inside_single_quote = False
    inside_double_quote = False

    indexes: range

    if reverse:
        indexes = range(start_idx - 1, -1, -1)
    else:
        indexes = range(start_idx, len(html))

    for i in indexes:
        c = html[i]

        # Toggle the quote flags when encountering quotes
        if c == "'" and not inside_double_quote:
            inside_single_quote = not inside_single_quote
        elif c == '"' and not inside_single_quote:
            inside_double_quote = not inside_double_quote

        # If we find a '<' and we're not inside quotes, we've found the start of a tag
        if not inside_single_quote and not inside_double_quote:
            if character is not None and c == character:
                return i
            elif character_regex_re is not None and character_regex_re.match(c):
                return i

    return -1
