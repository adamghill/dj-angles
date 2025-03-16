from dj_angles.mappers.angles import map_model
from tests.dj_angles.tags import create_tag


def test_as():
    expected = "{% model Book.objects.filter(id=1) as book %}"

    tag = create_tag("<dj-model code='Book.objects.filter(id=1)' as='book'>")
    actual = map_model(tag=tag)

    assert actual == expected


def test_no_as():
    expected = "{% model Book.objects.filter(id=1) %}"

    tag = create_tag("<dj-model code='Book.objects.filter(id=1)'>")
    actual = map_model(tag=tag)

    assert actual == expected


def test_end_tag():
    expected = ""

    tag = create_tag("</dj-model>")
    actual = map_model(tag=tag)

    assert actual == expected
