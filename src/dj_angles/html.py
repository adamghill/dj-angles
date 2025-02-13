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

    start_tag_idx = find_character(html, start_idx, "<", reverse=True)

    # If we found the start of the tag, extract the tag name
    if start_tag_idx != -1:
        for c in html[start_tag_idx + 1 : start_idx]:  # Start after '<'
            if c in (" ", ">"):
                break

            tag_name += c

    return (tag_name, start_tag_idx)


def find_character(html: str, start_idx: int, character: str, *, reverse: bool = False) -> int:
    inside_single_quote = False
    inside_double_quote = False

    indexes = []

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
        if c == character and not inside_single_quote and not inside_double_quote:
            return i

    return -1


def end_of_tag_index(html: str, start_idx: int, tag_name: str) -> int:
    if tag_name in VOID_ELEMENTS:
        idx = html.find("/>", start_idx)

        if idx > -1:
            return idx + 2

        idx = find_character(html, start_idx, ">")

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
