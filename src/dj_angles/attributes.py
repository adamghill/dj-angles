from collections.abc import Sequence
from typing import List, Optional

from dj_angles.tokenizer import yield_tokens


class Attribute:
    key: str
    value: str = None
    has_value: bool = False

    def __init__(self, attribute: str):
        tokens = tuple(yield_tokens(attribute, "="))

        if not tokens:
            raise Exception("Invalid attribute")

        self.key = tokens[0]

        if len(tokens) == 2:
            self.value = tokens[1]
            self.has_value = True

    def __str__(self):
        if self.value is None:
            return self.key

        return f"{self.key}={self.value}"


class Attributes(Sequence):
    def __init__(self, template_tag_args: str):
        self._attributes: List[Attribute] = []

        self.template_tag_args = template_tag_args
        self.parse()

    def parse(self):
        for arg in yield_tokens(self.template_tag_args, " "):
            template_tag_arg = Attribute(arg)
            self._attributes.append(template_tag_arg)

    def get(self, name: str, default=None) -> bool:
        for attribute in self._attributes:
            if attribute.key == name:
                return attribute

        return default

    def remove(self, key: str) -> None:
        _attributes = []

        for attribute in self._attributes:
            if attribute.key != key:
                _attributes.append(attribute)

        self._attributes = _attributes

    def pop(self, index: Optional[int] = None) -> Attribute:
        return self._attributes.pop(index)

    def prepend(self, attribute: str) -> None:
        _attribute = Attribute(attribute)

        if self.get(_attribute.key):
            raise Exception("Already existing attribute key")

        self._attributes.insert(0, _attribute)

    def append(self, attribute: str) -> None:
        _attribute = Attribute(attribute)

        if self.get(_attribute.key):
            raise Exception("Already existing attribute key")

        self._attributes.append(_attribute)

    def __getitem__(self, index: int):
        return self._attributes.__getitem__(index)

    def __iter__(self):
        return self._attributes.__iter__()

    def __len__(self):
        return self._attributes.__len__()

    def __str__(self):
        s = ""

        for attribute in self._attributes:
            s = f"{s} {attribute}"

        return s.strip()
