import pytest

from dj_angles.attributes import Attribute, Attributes
from dj_angles.exceptions import DuplicateAttributeError


def test_attribute_invalid_empty():
    with pytest.raises(Exception, match="Invalid attribute"):
        Attribute("")


def test_attributes_duplicate_append():
    attrs = Attributes()
    attrs.append("key=value")
    with pytest.raises(DuplicateAttributeError):
        attrs.append("key=value2")


def test_attributes_duplicate_prepend():
    attrs = Attributes()
    attrs.prepend("key=value")
    with pytest.raises(DuplicateAttributeError):
        attrs.prepend("key=value2")


def test_attributes_iter():
    attrs = Attributes("key=value")
    assert list(iter(attrs))


def test_token_count_assertion_error():
    with pytest.raises(AssertionError, match="Invalid number of tokens"):
        Attribute("key=value=extra")
