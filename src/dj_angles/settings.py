from typing import Any

from django.conf import settings


def get_setting(setting_name: str, default=None) -> Any:
    if not hasattr(settings, "ANGLES"):
        settings.ANGLES = {}

    if setting_name in settings.ANGLES:
        return settings.ANGLES[setting_name]

    return default
