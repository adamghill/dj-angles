from collections.abc import Sequence
from typing import SupportsIndex

from dj_angles.exceptions import DuplicateAttributeError, MissingAttributeError
from dj_angles.tokenizer import yield_tokens

VALID_ATTRIBUTE_TOKEN_COUNT = 2


class Attribute:
    """Encapsulates an attribute in an element. Attributes are a key-value pair, but the value can be
    `None`.

    Examples:
        - `<dj-include 'partial.html'>` has 1 attribute: `'partial.html'`. The value is `None`.
        - `<dj-include 'partial.html' shadow>` has 2 attributes: `'partial.html'` and `shadow`. The value is `None`.
        - `<dj-include 'partial.html' shadow test=True>` has 3 attributes: `'partial.html'`, `shadow`, `test`.\
            The first 2 attributes have a value of `None`, but `test` has a value of `True`.
    """

    key: str
    """Key of the attribute. Always defined."""

    value: str | None = None
    """Optional value of the attribute. Defaults to `None`."""

    has_value: bool = False
    """Whether or not the attribute has a value."""

    def __init__(self, attribute: str):
        tokens = tuple(yield_tokens(attribute, "="))

        if not tokens:
            raise Exception("Invalid attribute")
        elif len(tokens) > VALID_ATTRIBUTE_TOKEN_COUNT:
            raise AssertionError(f"Invalid number of tokens in attribute: '{attribute}'")

        self.key = tokens[0]

        if len(tokens) > 1:
            self.value = tokens[1]
            self.has_value = True

    def __str__(self):
        """Return the attribute as a string."""

        if self.value is None:
            return self.key

        return f"{self.key}={self.value}"


class Attributes(Sequence):
    """A list of attributes, usually inside a :obj:`~dj_angles.tags.Tag`."""

    template_tag_args: str
    """The original attributes as an unparsed string."""

    def __init__(self, template_tag_args: str = ""):
        self._attributes: dict[str, Attribute] = {}

        self.template_tag_args = template_tag_args
        self.parse()

    def parse(self):
        """Parse the attributes string to generate a list of :obj:`~dj_angles.attributes.Attribute` objects."""

        for arg in yield_tokens(self.template_tag_args, " "):
            arg = arg.strip()  # noqa: PLW2901

            if not arg:
                continue

            attribute = Attribute(arg)

            if attribute.key not in self._attributes:
                self._attributes[attribute.key] = attribute

    def has(self, name: str) -> bool:
        """Whether or not an there is an :obj:`~dj_angles.attributes.Attribute` by name.

        Args:
            param name: The name of the attribute.
        """

        return name in self._attributes

    def get(self, name: str) -> Attribute | None:
        """Get an :obj:`~dj_angles.attributes.Attribute` by name. Returns `None` if the attribute is missing.

        Args:
            param name: The name of the attribute.
            param default: What to return if the attribute is not available. Defaults to `None`.
        """

        return self._attributes.get(name)

    def remove(self, key: str) -> None:
        """Removes an attribute from the list.

        Args:
            param key: The key of the attribute to remove.

        Raises:
            :obj:`~dj_angles.exceptions.MissingAttributeError`: If the attribute is missing.
        """

        if key in self._attributes:
            del self._attributes[key]
        else:
            raise MissingAttributeError("Attribute was not found.")

    def pop_value(self, name: str) -> str | None:
        """Get the value of an :obj:`~dj_angles.attributes.Attribute` by name and remove the attribute from the tag
        attributes.

        Args:
            param name: The name of the attribute.
        """

        if (attribute := self.get(name)) is not None:
            del self._attributes[attribute.key]

            return attribute.value

        return None

    def pop(self, index: SupportsIndex) -> Attribute:
        """Remove and return the last attribute."""

        key = list(self._attributes.keys())[index]
        return self._attributes.pop(key)

    def prepend(self, attribute_string: str) -> None:
        """Parse the attribute string as an `Attribute` and add it to the beginning of the list of attributes.

        Args:
            param attribute_string: The attribute as a string.

        Raises:
            :obj:`~dj_angles.exceptions.DuplicateAttributeError`: If the attribute conflicts with an existing attribute.
        """

        _attribute = Attribute(attribute_string)

        if _attribute.key in self._attributes:
            raise DuplicateAttributeError("Already existing attribute key")

        self._attributes = {_attribute.key: _attribute, **self._attributes}

    def append(self, attribute_string: str) -> None:
        """Parse the attribute string as an `Attribute` and add it to the end of the list of attributes.

        Args:
            param attribute_string: The attribute as a string.

        Raises:
            :obj:`~dj_angles.exceptions.DuplicateAttributeError`: If the attribute conflicts with an existing attribute.
        """

        _attribute = Attribute(attribute_string)

        if _attribute.key in self._attributes:
            raise DuplicateAttributeError("Already existing attribute key")

        self._attributes[_attribute.key] = _attribute

    def __getitem__(self, index):
        return list(self._attributes.values())[index]

    def __iter__(self):
        return iter(self._attributes.values())

    def __len__(self):
        return len(self._attributes)

    def __str__(self):
        s = ""

        for attribute in self._attributes.values():
            s = f"{s} {attribute}"

        return s.strip()
