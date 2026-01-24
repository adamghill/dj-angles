from dj_angles.replacers.variables import replace_variables


def test_empty_variable_block():
    html = "{{ }}"
    assert replace_variables(html) == "{{ }}"


def test_empty_tokens_in_variable():
    html = "{{   }}"
    assert replace_variables(html) == "{{   }}"


def test_or_at_start():
    html = "{{ or B }}"
    assert replace_variables(html) == "{{ or B }}"  # Should not change as it fails validation


def test_or_at_end():
    html = "{{ A or }}"
    assert replace_variables(html) == "{{ A or }}"  # Should not change
