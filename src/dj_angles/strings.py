def dequotify(s: str) -> str:
    """Removes single or double quotes from a string.

    Args:
        param s: The string to remove quotes from.

    Returns:
        A new string without the quotes or the original if there were no quotes.
    """

    if (s.startswith("'") and s.endswith("'")) or (s.startswith('"') and s.endswith('"')):
        return s[1:-1]

    return s


def replace_newlines(s: str, replacement: str = "") -> str:
    """Replaces newlines with the given replacement string.

    Args:
        param s: The string to replace newlines in.
        param replacement: The string to replace the newlines with.

    Returns:
        A new string with the newlines replaced.
    """

    return s.replace("\r\n", replacement).replace("\n", replacement).replace("\r", replacement)
