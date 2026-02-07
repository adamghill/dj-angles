from dj_angles.replacers.comments import mask_comments


def test_mask_django_single_line():
    html = "Hello {# comment #} World"
    masked_html, comments = mask_comments(html)
    assert masked_html == "Hello __DJ_ANGLES_COMMENT_0__ World"
    assert comments == ["{# comment #}"]


def test_mask_django_block():
    html = "Hello {% comment %} block {% endcomment %} World"
    masked_html, comments = mask_comments(html)
    assert masked_html == "Hello __DJ_ANGLES_COMMENT_0__ World"
    assert comments == ["{% comment %} block {% endcomment %}"]


def test_mask_dj_comment():
    html = "Hello <dj-comment> custom </dj-comment> World"
    masked_html, comments = mask_comments(html)
    assert masked_html == "Hello __DJ_ANGLES_COMMENT_0__ World"
    assert comments == ["<dj-comment> custom </dj-comment>"]


def test_mask_nested_dj_comment():
    html = """
    <dj-comment>
        outer
        <dj-comment>
            inner
        </dj-comment>
        end outer
    </dj-comment>
    """
    masked_html, comments = mask_comments(html)
    assert "__DJ_ANGLES_COMMENT_0__" in masked_html
    assert len(comments) == 1
    assert "outer" in comments[0]
    assert "inner" in comments[0]


def test_mask_multiple_comments():
    html = "{# one #} middle <dj-comment> two </dj-comment> end"
    masked_html, comments = mask_comments(html)
    assert masked_html == "__DJ_ANGLES_COMMENT_0__ middle __DJ_ANGLES_COMMENT_1__ end"
    assert len(comments) == 2
    assert comments[0] == "{# one #}"
    assert comments[1] == "<dj-comment> two </dj-comment>"


def test_unclosed_comment():
    html = "Hello <dj-comment> unclosed"
    masked_html, comments = mask_comments(html)
    # Unclosed comments should be treated as text (not masked)
    assert masked_html == "Hello <dj-comment> unclosed"
    assert len(comments) == 0


def test_django_block_inside_dj_comment():
    html = "<dj-comment>{% comment %} inner {% endcomment %}</dj-comment>"
    masked_html, comments = mask_comments(html)
    assert masked_html == "__DJ_ANGLES_COMMENT_0__"
    assert len(comments) == 1
    assert "{% comment %}" in comments[0]


def test_mask_custom_prefix():
    html = "Hello <my-comment> custom </my-comment> World"
    # Use raw string for prefix to avoid escape issues in test
    masked_html, comments = mask_comments(html, initial_tag_regex=r"(my-)")
    assert masked_html == "Hello __DJ_ANGLES_COMMENT_0__ World"
    assert comments == ["<my-comment> custom </my-comment>"]


def test_mask_unclosed_tag():
    html = "Normal <dj-comment> This is unclosed"
    masked_html, comments = mask_comments(html)
    # Unclosed tags are kept as-is, not masked
    assert masked_html == html
    assert len(comments) == 0


def test_mask_orphaned_closing_tag():
    html = "Orphaned </dj-comment> tag"
    masked_html, comments = mask_comments(html)
    # Orphaned end tags should be masked to prevent downstream crashes
    assert masked_html == "Orphaned __DJ_ANGLES_COMMENT_0__ tag"
    assert comments == ["</dj-comment>"]


def test_mask_mixed_orphaned_tags():
    html = "</dj-comment> {% endcomment %}"
    masked_html, comments = mask_comments(html)
    assert masked_html == "__DJ_ANGLES_COMMENT_0__ __DJ_ANGLES_COMMENT_1__"
    assert comments == ["</dj-comment>", "{% endcomment %}"]
