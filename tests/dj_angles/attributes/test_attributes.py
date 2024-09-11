from dj_angles.attributes import Attributes


def test_single_quote():
    expected = "'partial.html'"
    actual = Attributes("'partial.html'")

    assert expected == actual[0].key


def test_double_quote():
    expected = '"partial.html"'
    actual = Attributes('"partial.html"')

    assert expected == actual[0].key


def test_attribute():
    actual = Attributes("rel='stylesheet'")

    assert "rel" == actual[0].key
    assert "'stylesheet'" == actual[0].value


def test_attribute_with_equal():
    actual = Attributes("rel='style=sheet'")

    assert "rel" == actual[0].key
    assert "'style=sheet'" == actual[0].value


def test_get():
    attributes = Attributes("rel='style=sheet'")
    actual = attributes.get("rel")

    assert "rel" == actual.key
    assert "'style=sheet'" == actual.value


def test_multiple_attributes():
    actual = Attributes("'partial.html' rel='stylesheet'")

    assert len(actual._attributes) == 2

    assert "'partial.html'" == actual._attributes[0].key
    assert actual._attributes[0].has_value is False

    assert "rel" == actual._attributes[1].key
    assert actual._attributes[1].has_value is True
    assert "'stylesheet'" == actual._attributes[1].value
