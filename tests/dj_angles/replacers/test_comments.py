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

    # If we want it to be ignored, this assertion should pass:
    assert "<dj-include 'fake-partial.html' />" in actual


def test_single_line_comment_ignored():
    template = "{# <dj-include 'fake-partial.html' /> #}"
    actual = convert_template(template)
    assert "<dj-include 'fake-partial.html' />" in actual


def test_custom_dj_comment_ignored():
    template = """
<dj-comment>
<dj-include 'fake-partial.html' />
</dj-comment>
"""
    actual = convert_template(template)

    assert "<dj-include 'fake-partial.html' />" in actual


def test_nested_dj_comments():
    template = """
    <dj-comment>
        Outer start
        <dj-comment>
            Inner
        </dj-comment>
        Outer end
        <dj-include 'should-be-ignored' />
    </dj-comment>
    """
    actual = convert_template(template)

    # Everything inside the top-level <dj-comment> should be ignored.
    # So we should see the original <dj-include ...> tag, NOT a processed result.
    assert "<dj-include 'should-be-ignored' />" in actual


def test_orphaned_closing_tag_does_not_crash():
    template = "Some content </dj-comment> and more content"
    # This should not raise IndexError: pop from an empty deque
    actual = convert_template(template)
    assert "</dj-comment>" in actual
