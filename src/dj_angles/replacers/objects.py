import logging
from dataclasses import dataclass

from dj_angles.tags import Tag

logger = logging.getLogger(__name__)


@dataclass(order=True)
class AtomicEdit:
    """An atomic edit to the HTML string."""

    position: int
    content: str
    is_insert: bool = True
    end_position: int = -1  # Only for deletions/replacements

    def apply(self, text: str) -> str:
        if self.is_insert:
            return text[: self.position] + self.content + text[self.position :]
        else:
            return text[: self.position] + self.content + text[self.end_position :]


def apply_edits(html: str, edits: list[AtomicEdit]) -> str:
    """Apply a list of atomic edits to the HTML string."""

    if not edits:
        return html

    # Sort edits by position ascending
    edits.sort(key=lambda x: x.position)

    # Reconstruct string by applying edits
    result_parts = []
    last_pos = 0

    for edit in edits:
        # Append original content up to this edit
        if edit.position > last_pos:
            result_parts.append(html[last_pos : edit.position])
            last_pos = edit.position

        # Apply the edit
        result_parts.append(edit.content)

        # Update position for replacements
        if not edit.is_insert:
            last_pos = max(last_pos, edit.end_position)

    # Append remaining content
    if last_pos < len(html):
        result_parts.append(html[last_pos:])

    return "".join(result_parts)


@dataclass
class Replacement:
    original: str
    replacement: str
    tag: Tag | None = None
    keep_endif: bool = False
    tag_start_idx: int = -1
