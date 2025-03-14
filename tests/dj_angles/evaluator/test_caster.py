from datetime import datetime, timedelta, timezone
from uuid import UUID

from dj_angles.evaluator import Caster


def test_caster_datetime():
    caster = Caster("2025-03-12T01:02:03")
    assert caster.cast() == datetime(2025, 3, 12, 1, 2, 3)  # noqa: DTZ001


def test_caster_datetime_tz():
    caster = Caster("2025-03-12T01:02:03+05:00")
    tzinfo = timezone(timedelta(seconds=18000))

    actual = caster.cast()
    assert actual == datetime(2025, 3, 12, 1, 2, 3, tzinfo=tzinfo)


def test_caster_uuid():
    caster = Caster("1ee49a9c-b83e-4a56-b02e-0d8ade93adcf")
    assert caster.cast() == UUID("1ee49a9c-b83e-4a56-b02e-0d8ade93adcf")


def test_caster_date():
    caster = Caster("2025-03-12")
    assert caster.cast() == datetime(2025, 3, 12)  # noqa: DTZ001


def test_caster_time():
    caster = Caster("2025-03-12")
    assert caster.cast() == datetime(2025, 3, 12)  # noqa: DTZ001


def test_caster_value_error():
    # This throws a ValueError because it looks like a UUID, but is not valid
    caster = Caster("1234567-1234-1234-1234-123456789123")
    assert caster.cast() == "1234567-1234-1234-1234-123456789123"


def test_caster_error():
    # This throws a TypeError from the datetime caster and an AttributeError from the UUID caster
    caster = Caster(1)
    assert caster.cast() == 1


# %d %H:%M:%S.%f
def test_caster_duration():
    caster = Caster("1 day, 2:3:4.567890")
    assert caster.cast() == timedelta(days=1, seconds=7384, microseconds=567890)
