from dj_angles.replacers.objects import AtomicEdit, apply_edits


def test_atomic_edit_apply_insert():
    edit = AtomicEdit(position=1, content="X")
    text = "abc"
    assert edit.apply(text) == "aXbc"


def test_atomic_edit_apply_replace():
    edit = AtomicEdit(position=1, content="X", is_insert=False, end_position=2)
    text = "abc"
    assert edit.apply(text) == "aXc"


def test_apply_edits_empty():
    assert apply_edits("abc", []) == "abc"


def test_apply_edits_inserts():
    edits = [
        AtomicEdit(position=1, content="X"),
        AtomicEdit(position=2, content="Y"),
    ]

    assert apply_edits("abc", edits) == "aXbYc"


def test_apply_edits_replace():
    edits = [
        AtomicEdit(position=1, content="X", is_insert=False, end_position=2),
    ]

    assert apply_edits("abc", edits) == "aXc"


def test_apply_edits_mixed():
    edits = [
        AtomicEdit(position=1, content="X"),
        AtomicEdit(position=2, content="Y", is_insert=False, end_position=3),
    ]

    assert apply_edits("abcd", edits) == "aXbYd"


def test_apply_edits_overlap_handing():
    edits = [
        AtomicEdit(position=1, content="X", is_insert=False, end_position=3),
        AtomicEdit(position=2, content="Y", is_insert=False, end_position=3),
    ]

    assert apply_edits("abcd", edits) == "aXYd"
