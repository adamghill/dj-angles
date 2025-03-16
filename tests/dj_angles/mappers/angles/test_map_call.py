from dj_angles.mappers.angles import map_call
from tests.dj_angles.tags import create_tag


def test_as():
    expected = '{% call slugify("Hello Goodbye") as slug %}'

    tag = create_tag("<dj-call code='slugify(\"Hello Goodbye\")' as='slug'>")
    actual = map_call(tag=tag)

    assert actual == expected


def test_no_as():
    expected = '{% call slugify("Hello Goodbye") %}'

    tag = create_tag("<dj-call code='slugify(\"Hello Goodbye\")'>")
    actual = map_call(tag=tag)

    assert actual == expected


def test_end_tag():
    expected = ""

    tag = create_tag("</dj-call>")
    actual = map_call(tag=tag)

    assert actual == expected
