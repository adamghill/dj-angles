from collections.abc import Generator


def yield_tokens(
    s: str, breaking_character: str, *, handle_quotes: bool = True, handle_parenthesis: bool = False
) -> Generator[str, None, None]:
    """Yields tokens from `s` by reading the string from left to right until a `breaking_character`,
    then continuing to read the `s` until the next `breaking_character`, ad infinitum.

    Args:
        param s: The string to parse.
        param breaking_character: The character that signifies the end of the token.
        param handle_quotes: Whether to ignore the breaking_character when inside single or double quotes.
        param handle_parenthesis: Whether to ignore the breaking_character when inside parenthesis.

    Returns:
        A generator of tokens.
    """

    in_double_quote = False
    in_single_quote = False
    parenthesis_count = 0
    token = ""

    for c in s:
        if c == "'" and handle_quotes:
            in_single_quote = not in_single_quote
        elif c == '"' and handle_quotes:
            in_double_quote = not in_double_quote
        elif c == "(" and handle_parenthesis:
            parenthesis_count += 1
        elif c == ")" and handle_parenthesis:
            parenthesis_count -= 1

        if c == breaking_character and not in_single_quote and not in_double_quote and parenthesis_count == 0:
            yield token
            token = ""
        else:
            token += c

    if token:
        yield token
