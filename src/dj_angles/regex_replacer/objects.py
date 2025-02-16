import logging
from dataclasses import dataclass

from dj_angles.tags import Tag

logger = logging.getLogger(__name__)


@dataclass
class Replacement:
    original: str
    replacement: str
    tag: Tag
    keep_endif: bool = False
    tag_start_idx: int = -1

    def __repr__(self):
        return f"Replacement(original={self.original!r}, replacement={self.replacement!r})"
