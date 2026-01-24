import pytest
from tests.dj_angles.tags import create_tag

from dj_angles.mappers.include import map_include


def test_include_missing_template_assertion():
    tag = create_tag("<dj-include>")
    with pytest.raises(AssertionError, match="must have an template name"):
        map_include(tag)


def test_include_unwrapped_end_tag():
    tag = create_tag("</dj-include>")
    tag.is_wrapped = False

    assert map_include(tag) == ""


def test_include_with_colon_in_filename():
    tag = create_tag("<dj-include 'folder:file.html'>")

    actual = map_include(tag)

    assert "folder.html" in actual
