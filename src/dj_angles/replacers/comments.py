import re


def mask_comments(html: str, initial_tag_regex: str = r"(dj-)") -> tuple[str, list[str]]:
    """Mask Django and custom comments in the HTML string.

    Args:
        html: The HTML string to process.
        initial_tag_regex: The regex for the tag prefix.

    Returns:
        A tuple containing the masked HTML string and a list of original comments.
    """
    comments = []

    # Combined pattern for all comment types
    # 1. Django comment block start: {% comment %}
    # 2. Django comment block end: {% endcomment %}
    # 3. Custom comment start: <prefix-comment>
    # 4. Custom comment end: </prefix-comment>
    # 5. Django single line comment: {# ... #}
    comment_pattern = re.compile(
        r"(?P<django_block_start>\{%\s*comment\s*%\})"
        r"|(?P<django_block_end>\{%\s*endcomment\s*%\})"
        r"|(?P<dj_comment_start><" + initial_tag_regex + r"comment(?:>|\s[^>]*>))"
        r"|(?P<dj_comment_end></" + initial_tag_regex + r"comment>)"
        r"|(?P<django_single>\{#.*?#\})",
        flags=re.IGNORECASE | re.DOTALL,
    )

    masked_html_parts = []
    last_pos = 0
    active_comment_start = None
    nesting_depth = 0
    in_django_block = False

    for match in comment_pattern.finditer(html):
        # If we are inside a Django block comment, we ONLY look for the end of THAT block
        if in_django_block:
            if match.group("django_block_end"):
                in_django_block = False

                if active_comment_start is not None:
                    full_comment = html[active_comment_start : match.end()]
                    comments.append(full_comment)
                    masked_html_parts.append(f"__DJ_ANGLES_COMMENT_{len(comments) - 1}__")
                    active_comment_start = None
                    last_pos = match.end()
            continue

        # If we are inside a dj-comment block, manage nesting depth
        if nesting_depth > 0:
            if match.group("dj_comment_start"):
                nesting_depth += 1
            elif match.group("dj_comment_end"):
                nesting_depth -= 1

                if nesting_depth == 0:
                    if active_comment_start is not None:
                        full_comment = html[active_comment_start : match.end()]
                        comments.append(full_comment)
                        masked_html_parts.append(f"__DJ_ANGLES_COMMENT_{len(comments) - 1}__")
                        active_comment_start = None
                        last_pos = match.end()
            continue

        # Not currently in any comment, looking for start
        if match.group("django_single"):
            # Single line comment - immediate replacement
            masked_html_parts.append(html[last_pos : match.start()])
            full_comment = match.group(0)
            comments.append(full_comment)
            masked_html_parts.append(f"__DJ_ANGLES_COMMENT_{len(comments) - 1}__")
            last_pos = match.end()

        elif match.group("django_block_start"):
            # Start of Django block
            masked_html_parts.append(html[last_pos : match.start()])
            active_comment_start = match.start()
            last_pos = match.start()  # Set last_pos to start of unclosed block
            in_django_block = True

        elif match.group("dj_comment_start"):
            # Start of dj-comment
            masked_html_parts.append(html[last_pos : match.start()])
            active_comment_start = match.start()
            last_pos = match.start()  # Set last_pos to start of unclosed block
            nesting_depth = 1

        elif match.group("django_block_end") or match.group("dj_comment_end"):
            # Orphaned end tag - mask it to prevent crashes in subsequent replacers
            masked_html_parts.append(html[last_pos : match.start()])
            full_comment = match.group(0)
            comments.append(full_comment)
            masked_html_parts.append(f"__DJ_ANGLES_COMMENT_{len(comments) - 1}__")
            last_pos = match.end()

    # Add remaining text (either everything since last match, or the unclosed block)
    masked_html_parts.append(html[last_pos:])

    return "".join(masked_html_parts), comments
