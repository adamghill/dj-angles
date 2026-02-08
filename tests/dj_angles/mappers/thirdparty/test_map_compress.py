from dj_angles.mappers.thirdparty import map_compress
from tests.dj_angles.tags import create_tag


def test_css():
    expected = "{% compress css %}"

    html = "<dj-compress css>"
    tag = create_tag(html)

    actual = map_compress(tag=tag)

    assert actual == expected


def test_js():
    expected = "{% compress js %}"

    html = "<dj-compress js>"
    tag = create_tag(html)

    actual = map_compress(tag=tag)

    assert actual == expected


def test_is_closing():
    expected = "{% endcompress %}"

    html = "</dj-compress>"
    tag = create_tag(html)

    actual = map_compress(tag=tag)

    assert actual == expected


def test_css_inline():
    expected = "{% compress css inline %}"

    html = "<dj-compress css inline>"
    tag = create_tag(html)

    actual = map_compress(tag=tag)

    assert actual == expected


def test_js_inline():
    expected = "{% compress js inline %}"

    html = "<dj-compress js inline>"
    tag = create_tag(html)

    actual = map_compress(tag=tag)

    assert actual == expected


def test_type_attribute():
    expected = "{% compress js %}"

    html = "<dj-compress type='js'>"
    tag = create_tag(html)

    actual = map_compress(tag=tag)

    assert actual == expected


def test_default_to_css():
    expected = "{% compress css %}"

    html = "<dj-compress>"
    tag = create_tag(html)

    actual = map_compress(tag=tag)

    assert actual == expected


def test_css_file():
    expected = "{% compress css file %}"

    html = "<dj-compress css file>"
    tag = create_tag(html)

    actual = map_compress(tag=tag)

    assert actual == expected


def test_js_preload():
    expected = "{% compress js preload %}"

    html = "<dj-compress js preload>"
    tag = create_tag(html)

    actual = map_compress(tag=tag)

    assert actual == expected


def test_with_block_name():
    expected = "{% compress css inline my-styles %}"

    html = "<dj-compress css inline name='my-styles'>"
    tag = create_tag(html)

    actual = map_compress(tag=tag)

    assert actual == expected
