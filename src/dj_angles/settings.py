import re
from functools import lru_cache
from typing import Any

from django.conf import settings


def get_setting(setting_name: str, key_path: str = "", default: Any = None) -> Any:
    """Get a setting from the `ANGLES` dictionary in settings.

    Args:
        param setting_name: The name of the setting.
        param key_path: The name of the sub-dictionary under `ANGLES`.
        param default: The value that should be returned if the setting is missing.
    """

    if not hasattr(settings, "ANGLES"):
        settings.ANGLES = {}

    data = settings.ANGLES

    if key_path:
        if key_path not in data:
            data[key_path] = {}

        data = data[key_path]

    if setting_name in data:
        return data[setting_name]

    return default


def get_tag_regex():
    """Gets a compiled regex based on the `initial_tag_regex` setting or default of r'(dj-)'."""

    initial_tag_regex = get_setting("initial_tag_regex", default=r"(dj-)")

    if initial_tag_regex is None:
        initial_tag_regex = ""

    tag_regex = rf"</?({initial_tag_regex}(?P<tag_name>[^\s>]+))\s*(?P<template_tag_args>.*?)\s*/?>"

    @lru_cache(maxsize=32)
    def _compile_regex(_tag_regex):
        """Silly internal function to cache the compiled regex."""

        return re.compile(_tag_regex, re.DOTALL)

    return _compile_regex(tag_regex)
