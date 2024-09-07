from dj_angles.mappers import map_include


def test_not_self_closing():
    expected = "<dj-partial>{% include 'partial.html' %}"
    actual = map_include(component_name="include", template_tag_args="'partial'", is_tag_self_closing=False)

    assert actual == expected


def test_single_quotes():
    expected = "<dj-partial>{% include 'partial.html' %}</dj-partial>"
    actual = map_include(component_name="include", template_tag_args="'partial'", is_tag_self_closing=True)

    assert actual == expected


def test_double_quotes():
    expected = '<dj-partial>{% include "partial.html" %}</dj-partial>'
    actual = map_include(component_name="include", template_tag_args='"partial"', is_tag_self_closing=True)

    assert actual == expected


def test_extension():
    expected = "<dj-partial>{% include 'partial.html' %}</dj-partial>"
    actual = map_include(component_name="include", template_tag_args="'partial.html'", is_tag_self_closing=True)

    assert actual == expected


def test_directory():
    expected = "<dj-more-partial>{% include 'more/partial.html' %}</dj-more-partial>"
    actual = map_include(component_name="include", template_tag_args="'more/partial'", is_tag_self_closing=True)

    assert actual == expected


def test_shadow():
    expected = "<dj-partial><template shadowrootmode='open'>{% include 'partial.html' %}</template></dj-partial>"
    actual = map_include(component_name="include", template_tag_args="'partial' shadow", is_tag_self_closing=True)

    assert actual == expected
