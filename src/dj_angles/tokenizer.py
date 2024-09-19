from typing import Generator


def yield_tokens(s: str, breaking_character: str) -> Generator[str, None, None]:
    """Yields tokens from `s` by reading the string from left to right until a `breaking_character`,
    then continuing to read the `s` until the next `breaking_character`, ad infinitum.

    Args:
        param s: The string to parse.
        param breaking_character: The character that signifies the end of the token.

    Returns:
        A generator of tokens.
    """

    in_double_quote = False
    in_single_quote = False
    token = ""

    for c in s:
        if c == "'":
            in_single_quote = not in_single_quote
        elif c == '"':
            in_double_quote = not in_double_quote

        if c == breaking_character and not in_single_quote and not in_double_quote:
            yield token
            token = ""
        else:
            token += c

    if token:
        yield token
