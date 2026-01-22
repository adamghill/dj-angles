"""Shared utilities for tracking quote state during string parsing."""


class QuoteTracker:
    """Tracks whether we're inside single or double quotes during character-by-character parsing."""

    QUOTE_CHARS = ("'", '"')

    def __init__(self) -> None:
        self.in_single_quote = False
        self.in_double_quote = False

    @staticmethod
    def is_quote_char(char: str) -> bool:
        """Return True if the character is a quote character."""
        return char in QuoteTracker.QUOTE_CHARS

    def update(self, char: str) -> None:
        """Update quote state based on the current character."""
        if char == "'" and not self.in_double_quote:
            self.in_single_quote = not self.in_single_quote
        elif char == '"' and not self.in_single_quote:
            self.in_double_quote = not self.in_double_quote

    @property
    def inside_quotes(self) -> bool:
        """Return True if currently inside any type of quote."""
        return self.in_single_quote or self.in_double_quote

    def reset(self) -> None:
        """Reset the quote state."""
        self.in_single_quote = False
        self.in_double_quote = False
