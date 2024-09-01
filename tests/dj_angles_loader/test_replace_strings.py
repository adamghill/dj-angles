from dj_angles.template_loader import replace_strings


def test_replace_strings():
    expected = """{% extends 'base.html' %}
"""
    actual = replace_strings("""<dj-extends 'base.html' />
""")

    assert actual == expected
