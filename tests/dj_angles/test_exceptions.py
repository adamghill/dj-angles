from dj_angles.exceptions import (
    DuplicateAttributeError,
    InvalidAttributeError,
    InvalidEndTagError,
    MissingAttributeError,
)


class MockTag:
    pass


def test_invalid_end_tag_error():
    tag = MockTag()
    last_tag = MockTag()
    e = InvalidEndTagError(tag, last_tag)
    assert e.tag == tag
    assert e.last_tag == last_tag


def test_missing_attribute_error():
    e = MissingAttributeError("foo")
    assert e.name == "foo"


def test_duplicate_attribute_error():
    e = DuplicateAttributeError("foo")
    assert e.name == "foo"


def test_invalid_attribute_error():
    e = InvalidAttributeError("foo", "message")
    assert e.name == "foo"
    assert str(e) == "message"
