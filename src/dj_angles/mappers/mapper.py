from collections import UserDict
from collections.abc import Callable
from typing import Optional, Union

from django.utils.module_loading import import_string

from dj_angles.mappers.angles import map_call, map_model
from dj_angles.mappers.django import map_autoescape, map_block, map_css, map_extends, map_image
from dj_angles.mappers.include import map_include
from dj_angles.modules import is_module_available
from dj_angles.settings import get_setting

TAG_NAME_TO_DJANGO_TEMPLATE_TAG_MAP: dict[Optional[str], Union[Callable, str]] = {
    "extends": map_extends,
    "block": map_block,
    "verbatim": "verbatim",
    "include": map_include,
    "comment": "comment",
    "#": "comment",
    "autoescape-on": map_autoescape,
    "autoescape-off": map_autoescape,
    "csrf-token": "csrf_token",
    "csrf": "csrf_token",
    "csrf-input": "csrf_token",
    "debug": "debug",
    "filter": "filter",
    "lorem": "lorem",
    "now": "now",
    "spaceless": "spaceless",
    "templatetag": "templatetag",
    "image": map_image,
    "css": map_css,
    "model": map_model,
    "call": map_call,
}
"""Default mappings for tag names to Django template tags."""

tag_map: Optional["TagMap"] = None


class TagMap(UserDict):
    def __init__(self) -> None:
        super().__init__()

        self.data: dict[Optional[str], Union[Callable, str]] = TAG_NAME_TO_DJANGO_TEMPLATE_TAG_MAP.copy()

        # Add bird if installed
        self.add_module_mapper("django_bird", "bird", "dj_angles.mappers.map_bird")

        # Add custom mappers if they are defined in settings
        self.add_custom_mappers()

        # Add default mapper if it is defined in the settings
        self.add_default_mapper()

        # Convert string values to imports if possible
        self.import_strings()

    def add_custom_mappers(self) -> None:
        """Get custom mappers from settings and add it to the tag map."""

        mappers = get_setting("mappers", default={})

        if not isinstance(mappers, dict):
            raise AssertionError("ANGLES.mappers must be a dictionary")

        self.data.update(mappers)

    def add_default_mapper(self) -> None:
        """Add default mapper if in settings, or fallback to the default mapper."""

        default_mapper = get_setting("default_mapper", "dj_angles.mappers.default_mapper")

        if default_mapper is not None:
            # Add the default with a magic key of `None`
            self.data.update({None: import_string(default_mapper)})

    def import_strings(self):
        """Try importing any values that are strings."""

        for key, value in self.data.items():
            if isinstance(value, str):
                try:
                    self.data[key] = import_string(value)
                except ImportError:
                    pass

    def add_module_mapper(self, module: str, tag_name: str, mapper: Union[str, Callable]) -> None:
        """Add module mappers depending on whether the module is installed or not."""

        if is_module_available(module):
            self.data.update({tag_name: mapper})


def get_tag_map() -> TagMap:
    """Get the complete tag map based on the default, dynamic, and settings mappers."""

    global tag_map  # noqa: PLW0603

    if tag_map is None:
        tag_map = TagMap()

    return tag_map


def clear_tag_map() -> None:
    """Clear the generated tag map so that it will be re-generated. Useful for tests."""

    global tag_map  # noqa: PLW0603
    tag_map = None
