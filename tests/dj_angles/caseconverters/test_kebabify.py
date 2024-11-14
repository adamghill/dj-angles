import pytest

from dj_angles.caseconverter import kebabify


@pytest.mark.parametrize(
    "input, expect",
    [
        # With punctuation.
        ("Hello, world!", "hello-world"),
        # Camel cased
        ("helloWorld", "hello-world"),
        # Joined by delimeter.
        ("Hello-World", "hello-world"),
        # Cobol cased
        ("HELLO-WORLD", "hello-world"),
        # Without punctuation.
        ("Hello world", "hello-world"),
        # Repeating single delimeter
        ("Hello   World", "hello-world"),
        # Repeating delimeters of different types
        ("Hello -__  World", "hello-world"),
        # Wrapped in delimeter
        (" hello world ", "hello-world"),
        # End in capital letter
        ("hellO", "hell-o"),
        # Long sentence with punctuation
        (
            r"the quick !b@rown fo%x jumped over the laZy Do'G",
            "the-quick-brown-fox-jumped-over-the-la-zy-do-g",
        ),
        # Alternating character cases
        ("heLlo WoRld", "he-llo-wo-rld"),
    ],
)
def test_default(input, expect):
    assert kebabify(input) == expect


@pytest.mark.parametrize(
    "input, expect",
    [
        # With punctuation.
        ("component/partial", "component/partial"),
        # With extension
        ("component/partial.html", "component/partial.html"),
        # Pascal cased
        ("PartialOne", "partial-one"),
    ],
)
def test_keep_punctuation(input, expect):
    assert kebabify(input, strip_punctuation=False) == expect
