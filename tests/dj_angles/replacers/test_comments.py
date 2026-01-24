from dj_angles.replacers import convert_template


def test_commented_out_tag_is_ignored():
    template = """
{% comment %}
<dj-include 'fake-partial.html' />
{% endcomment %}
"""
    # If ignored, it should remain as <dj-include ...> inside the comment
    # If processed, it will become {% include ... %}

    # We expect it to NOT be processed if the goal is to ignore comments.
    # But currently we want to see what happens.

    actual = convert_template(template)

    # Let's see what we get. I suspect it currently converts it.
    print(f"\nACTUAL:\n{actual}")

    # If we want it to be ignored, this assertion should pass:
    assert "<dj-include 'fake-partial.html' />" in actual


def test_single_line_comment_ignored():
    template = "{# <dj-include 'fake-partial.html' /> #}"
    actual = convert_template(template)
    print(f"\nACTUAL SINGLE LINE:\n{actual}")
    assert "<dj-include 'fake-partial.html' />" in actual


def test_custom_dj_comment_ignored():
    template = """
<dj-comment>
<dj-include 'fake-partial.html' />
</dj-comment>
"""
    actual = convert_template(template)
    print(f"\nACTUAL DJ-COMMENT:\n{actual}")
    assert "<dj-include 'fake-partial.html' />" in actual
