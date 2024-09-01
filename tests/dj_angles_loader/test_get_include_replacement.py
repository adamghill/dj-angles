from dj_angles.template_loader import get_include_replacement


def test_typical():
    expected = "{% include 'partial.html' %}"
    actual = get_include_replacement("partial", is_shadow=False)

    assert actual == expected


def test_single_quotes():
    expected = "{% include 'partial.html' %}"
    actual = get_include_replacement("'partial.html'", is_shadow=False)

    assert actual == expected


def test_double_quotes():
    expected = '{% include "partial.html" %}'
    actual = get_include_replacement('"partial.html"', is_shadow=False)

    assert actual == expected


def test_extension():
    expected = "{% include 'partial.html' %}"
    actual = get_include_replacement("partial.html", is_shadow=False)

    assert actual == expected


def test_directory():
    expected = "{% include 'more/partial.html' %}"
    actual = get_include_replacement("more/partial", is_shadow=False)

    assert actual == expected


def test_shadow():
    expected = "<template shadowrootmode='open'>{% include 'partial.html' %}</template>"
    actual = get_include_replacement("partial", is_shadow=True, is_tag_self_closing=True)

    assert actual == expected
