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
