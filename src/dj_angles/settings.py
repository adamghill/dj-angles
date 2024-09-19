from typing import Any

from django.conf import settings


def get_setting(setting_name: str, default=None) -> Any:
    """Get a `dj-angles` setting from the `ANGLES` setting dictionary.

    Args:
        param setting_name: The name of the setting.
        param default: The value that should be returned if the setting is missing.
    """

    if not hasattr(settings, "ANGLES"):
        settings.ANGLES = {}

    if setting_name in settings.ANGLES:
        return settings.ANGLES[setting_name]

    return default
