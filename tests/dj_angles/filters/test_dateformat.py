from datetime import datetime, timezone

from dj_angles.templatetags.dj_angles import dateformat


def test_p():
    expected = "PM"

    dt = datetime(2025, 3, 15, 14, 3, 6, tzinfo=timezone.utc)
    actual = dateformat(dt, "%p")

    assert actual == expected


def test_d():
    expected = "15"

    dt = datetime(2025, 3, 15, 14, 3, 6, tzinfo=timezone.utc)
    actual = dateformat(dt, "%d")

    assert actual == expected
