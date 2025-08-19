from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from dj_angles.tags import Tag


class InvalidEndTagError(Exception):
    """Indicates that a tag has been opened, but not closed correctly."""

    tag: "Tag"
    """Current tag that is being processed."""

    last_tag: "Tag"
    """The previous tag that was processed."""

    def __init__(self, tag: "Tag", last_tag: "Tag"):
        super().__init__()

        self.tag = tag
        self.last_tag = last_tag


class MissingAttributeError(Exception):
    """Indicates that an attribute could not be found."""

    name: str
    """The name of the attribute."""

    def __init__(self, name: str):
        super().__init__()

        self.name = name


class DuplicateAttributeError(Exception):
    """Indicates that an attribute would be duplicated."""

    name: str
    """The name of the attribute."""

    def __init__(self, name: str):
        super().__init__()

        self.name = name


class InvalidAttributeError(Exception):
    """Indicates that an attribute is invalid."""

    name: str
    """The name of the attribute."""

    def __init__(self, name: str, message: Optional[str] = None):
        super().__init__(message)

        self.name = name
