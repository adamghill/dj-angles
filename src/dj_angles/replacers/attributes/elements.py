import re
from dataclasses import dataclass
from typing import Optional

from dj_angles.htmls import VOID_ELEMENTS
from dj_angles.replacers.objects import AtomicEdit


@dataclass
class Element:
    """Represents an HTML element with a dj-* attribute."""

    tag_name: str
    """Name of the HTML tag, e.g. ``div`` or ``img``."""

    tag_start: int
    """Position of the ``<`` that starts the opening tag in the original HTML."""

    tag_end: int
    """Position just after the ``>`` that ends the opening tag."""

    full_end: int
    """Position just after the element's closing tag, or ``tag_end`` for void/self-closing tags."""

    original_tag: str
    """The original opening tag string, including the dj-* attribute."""

    original_full: str
    """The full original element, from the opening tag through the closing tag."""

    attr_match: re.Match
    """Regex match for the dj-* attribute that triggered this element's discovery."""

    type: str
    """The dj-* attribute type, e.g. ``if``, ``elif``, ``else``, or ``value``."""

    value: str = ""
    """The value of the dj-* attribute, e.g. the condition for ``dj-if`` or the variable for ``dj-value``."""

    @classmethod
    def from_match(cls, html: str, match: re.Match, attr_type: str) -> "Element":
        """Find the HTML element containing a dj-* attribute match and return an instance."""

        tag_start = html.rfind("<", 0, match.start())
        tag_end = html.find(">", match.end()) + 1
        full_end = cls._find_end(html, tag_start, tag_end)

        original_tag = html[tag_start:tag_end]
        original_full = html[tag_start:full_end]

        tag_match = re.match(r"</?(\w+)", original_tag)
        tag_name = tag_match.group(1) if tag_match else ""

        return cls(
            tag_name=tag_name,
            tag_start=tag_start,
            tag_end=tag_end,
            full_end=full_end,
            original_tag=original_tag,
            original_full=original_full,
            attr_match=match,
            type=attr_type,
        )

    @property
    def is_closing(self) -> bool:
        """Whether the element is a closing tag."""
        return self.original_tag.startswith("</")

    def remove_attribute(self) -> str:
        """Remove the dj-* attribute from the tag."""
        attr_start_in_tag = self.attr_match.start() - self.tag_start
        attr_end_in_tag = self.attr_match.end() - self.tag_start

        new_tag = self.original_tag[:attr_start_in_tag] + self.original_tag[attr_end_in_tag:]

        new_tag = re.sub(r"\s+>", ">", new_tag)
        new_tag = re.sub(r"\s{2,}", " ", new_tag)

        return new_tag

    def contains(self, other: "Element") -> bool:
        """Whether this element fully contains another element."""
        return self.tag_start <= other.tag_start and other.full_end <= self.full_end

    def closing_tag(self) -> str:
        """Return the existing closing tag or generate one."""
        matches = list(re.finditer(rf"</{self.tag_name}\s*>", self.original_full, re.IGNORECASE))
        return matches[-1].group(0) if matches else f"</{self.tag_name}>"

    def make_edit(self, content: str, *, replace: bool = False) -> AtomicEdit:
        """Convenience: insert ``content`` at ``tag_start``, optionally replacing the opening tag."""
        if replace:
            return AtomicEdit(position=self.tag_start, content=content, is_insert=False, end_position=self.tag_end)
        return AtomicEdit(position=self.tag_start, content=content)

    @staticmethod
    def _find_end(html: str, tag_start: int, tag_end: int) -> int:
        """Find the position just after the element's closing tag."""

        tag_html = html[tag_start:tag_end]
        tag_match = re.match(r"<(\w+)", tag_html)

        if not tag_match:
            return tag_end

        tag_name = tag_match.group(1)

        if tag_html.rstrip().endswith("/>"):
            return tag_end

        if tag_name.lower() in VOID_ELEMENTS:
            return tag_end

        depth = 1
        pos = tag_end
        pattern = re.compile(rf"<(/)?{tag_name}(?:\s[^>]*)?\s*/?>", re.IGNORECASE)

        while depth > 0 and pos < len(html):
            m = pattern.search(html, pos)

            if not m:
                break

            if m.group(1):
                depth -= 1
            elif not m.group(0).endswith("/>"):
                depth += 1

            pos = m.end()

        return pos


@dataclass
class ConditionalElement(Element):
    """Represents an element with a dj-if/elif/else attribute."""

    chain_id: int = -1
    next_in_chain: Optional["ConditionalElement"] = None

    @property
    def condition(self) -> str:
        """The condition value of the attribute (empty for else)."""
        return self.value


@dataclass
class ForElement(Element):
    """Represents an element with a dj-for/dj-empty/dj-endfor attribute."""

    empty_sibling: Optional["ForElement"] = None
    """The linked dj-empty element, if any."""
