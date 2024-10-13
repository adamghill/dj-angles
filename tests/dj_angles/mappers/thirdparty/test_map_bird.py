from dj_angles.mappers.thirdparty import map_bird
from tests.dj_angles.tags import create_tag


def test_not_self_closing():
    expected = "{% bird 'partial' %}"

    html = "<dj-bird 'partial'>"
    tag = create_tag(html)

    actual = map_bird(tag=tag)

    assert actual == expected


def test_is_closing():
    expected = "{% endbird %}"

    html = "</dj-bird>"
    tag = create_tag(html)

    actual = map_bird(tag=tag)

    assert actual == expected


def test_self_closing():
    expected = "{% bird 'partial' / %}"

    html = "<dj-bird 'partial' />"
    tag = create_tag(html)

    actual = map_bird(tag=tag)

    assert actual == expected


def test_template_attribute():
    expected = "{% bird 'partial' / %}"

    html = "<dj-bird template='partial' />"
    tag = create_tag(html)

    actual = map_bird(tag=tag)

    assert actual == expected


def test_additional_attribute():
    expected = "{% bird 'partial' blob='test' %}"

    html = "<dj-bird template='partial' blob='test'>"
    tag = create_tag(html)

    actual = map_bird(tag=tag)

    assert actual == expected
