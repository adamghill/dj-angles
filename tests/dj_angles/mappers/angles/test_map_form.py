from dj_angles.mappers.angles import map_form
from tests.dj_angles.tags import create_tag


def test_start_tag():
    expected = "<form action='/submit' method='POST'>"

    html = "<dj-form action='/submit' method='POST'>"
    tag = create_tag(html)
    actual = map_form(tag=tag)

    assert actual == expected


def test_csrf():
    expected = "<form action='/submit' method='POST'>{% csrf_token %}"

    html = "<dj-form action='/submit' method='POST' csrf>"
    tag = create_tag(html)
    actual = map_form(tag=tag)

    assert actual == expected


def test_ajax():
    expected = "<ajax-form swap='outerHTML' delay='0'><form action='/submit' method='POST'>"

    html = "<dj-form action='/submit' method='POST' ajax>"
    tag = create_tag(html)
    actual = map_form(tag=tag)

    assert actual == expected


def test_swap():
    expected = "<ajax-form swap='outerHTML' delay='0'><form action='/submit' method='POST'>"

    html = "<dj-form action='/submit' method='POST' ajax swap='outerHTML'>"
    tag = create_tag(html)
    actual = map_form(tag=tag)

    assert actual == expected


def test_additional_attributes():
    expected = "<form action='/submit' method='POST' class='my-class'>"

    html = "<dj-form action='/submit' method='POST' class='my-class'>"
    tag = create_tag(html)
    actual = map_form(tag=tag)

    assert actual == expected


def test_end():
    expected = "</form>"

    tag = create_tag("</dj-form>")
    tag.start_tag = create_tag("<dj-form>")
    actual = map_form(tag=tag)

    assert actual == expected


def test_end_ajax():
    expected = "</ajax-form></form>"

    tag = create_tag("</dj-form>")
    tag.start_tag = create_tag("<dj-form ajax>")
    actual = map_form(tag=tag)

    assert actual == expected
