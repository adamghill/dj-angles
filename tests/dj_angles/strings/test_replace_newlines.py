from dj_angles.strings import replace_newlines


def test_replace_newlines():
    assert replace_newlines("\r\n") == ""
    assert replace_newlines("\n") == ""
    assert replace_newlines("\r") == ""
    assert replace_newlines("\r\n\r\n\n\n") == ""


def test_replace_newlines_with_string():
    assert replace_newlines("\r\n", "c") == "c"
    assert replace_newlines("\n", "c") == "c"
    assert replace_newlines("\r", "c") == "c"
    assert replace_newlines("\r\n\r\n\n\n", "c") == "cccc"
