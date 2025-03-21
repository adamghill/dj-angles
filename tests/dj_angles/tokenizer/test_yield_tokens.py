from dj_angles.tokenizer import yield_tokens


def test_single_quote():
    expected = "'partial.html'"
    actual = yield_tokens("'partial.html'", " ")

    assert expected == next(actual)


def test_double_quote():
    expected = '"partial.html"'
    actual = yield_tokens('"partial.html"', " ")

    assert expected == next(actual)


def test_breaking_character():
    expected = ("rel", "'stylesheet'")
    actual = yield_tokens("rel='stylesheet'", "=")

    assert expected == tuple(actual)


def test_breaking_character_inside_single_quote():
    expected = ("rel", "'style=sheet'")
    actual = yield_tokens("rel='style=sheet'", "=")

    assert expected == tuple(actual)


def test_breaking_character_inside_parenthesis():
    expected = ("set_name('hello', 'world')", "another_something('ok', 'cool')")
    actual = yield_tokens("set_name('hello', 'world') another_something('ok', 'cool')", " ", handle_parenthesis=True)

    assert expected == tuple(actual)


def test_breaking_character_inside_multiple_parenthesis():
    expected = (
        "set_name('hello', 'world')",
        "another_something((('ok'), ('cool')))",
    )
    actual = yield_tokens(
        "set_name('hello', 'world') another_something((('ok'), ('cool')))", " ", handle_parenthesis=True
    )

    assert expected == tuple(actual)
