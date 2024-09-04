from dj_angles.replacer import replace_django_templatetags


def test_extends():
    expected = """{% extends 'base.html' %}
"""
    actual = replace_django_templatetags("""<dj-extends 'base.html' />
""")

    assert actual == expected
