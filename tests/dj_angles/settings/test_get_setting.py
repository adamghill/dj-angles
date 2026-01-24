from django.conf import settings

from dj_angles.settings import get_setting


def test_get_setting_init_angles():
    # Ensure ANGLES is not set
    if hasattr(settings, "ANGLES"):
        del settings.ANGLES

    val = get_setting("MISSING")
    assert val is None
    assert hasattr(settings, "ANGLES")
    assert settings.ANGLES == {}
