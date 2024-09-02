from dj_angles.replacer import get_include_replacement


def test_typical():
    expected = "<dj-partial>{% include 'partial.html' %}</dj-partial>"
    actual = get_include_replacement("partial", is_shadow=False, is_tag_self_closing=True)

    assert actual == expected


def test_not_self_closing():
    expected = "<dj-partial>{% include 'partial.html' %}"
    actual = get_include_replacement("partial", is_shadow=False, is_tag_self_closing=False)

    assert actual == expected


def test_single_quotes():
    expected = "<dj-partial>{% include 'partial.html' %}</dj-partial>"
    actual = get_include_replacement("'partial.html'", is_shadow=False, is_tag_self_closing=True)

    assert actual == expected


def test_double_quotes():
    expected = '<dj-partial>{% include "partial.html" %}</dj-partial>'
    actual = get_include_replacement('"partial.html"', is_shadow=False, is_tag_self_closing=True)

    assert actual == expected


def test_extension():
    expected = "<dj-partial>{% include 'partial.html' %}</dj-partial>"
    actual = get_include_replacement("partial.html", is_shadow=False, is_tag_self_closing=True)

    assert actual == expected


def test_directory():
    expected = "<dj-more-partial>{% include 'more/partial.html' %}</dj-more-partial>"
    actual = get_include_replacement("more/partial", is_shadow=False, is_tag_self_closing=True)

    assert actual == expected


def test_shadow():
    expected = "<dj-partial><template shadowrootmode='open'>{% include 'partial.html' %}</template></dj-partial>"
    actual = get_include_replacement("partial", is_shadow=True, is_tag_self_closing=True)

    assert actual == expected
