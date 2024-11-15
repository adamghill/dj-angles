from collections.abc import Callable
from typing import Optional, Union

from django.utils.module_loading import import_string

from dj_angles.mappers.django import map_autoescape, map_block, map_css, map_extends, map_image
from dj_angles.mappers.include import map_include
from dj_angles.mappers.thirdparty import map_bird
from dj_angles.modules import is_module_available
from dj_angles.settings import get_setting

TAG_NAME_TO_DJANGO_TEMPLATE_TAG_MAP: Optional[dict[Optional[str], Union[Callable, str]]] = {
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
}
"""Default mappings for tag names to Django template tags."""

tag_map: Optional[dict[Optional[str], Union[Callable, str]]] = None


def get_tag_map() -> Optional[dict[Optional[str], Union[Callable, str]]]:
    """Get the complete tag map based on the default, dynamic, and settings mappers."""

    global tag_map  # noqa: PLW0603

    if tag_map is None:
        tag_map = TAG_NAME_TO_DJANGO_TEMPLATE_TAG_MAP.copy()

        if tag_map is None:
            raise AssertionError("Invalid tag_map")

        # Add bird if installed
        if is_module_available("django_bird"):
            tag_map.update({"bird": map_bird})

        # Add dynamic mappers if in settings
        mappers = get_setting("mappers", default={})

        if not isinstance(mappers, dict):
            raise AssertionError("ANGLES.mappers must be a dictionary")

        tag_map.update(mappers)

        # Add default mapper if in settings, or fallback to the default mapper
        default_mapper = get_setting("default_mapper", "dj_angles.mappers.angles.default_mapper")

        if default_mapper is not None:
            # Add the default with a magic key of `None`
            tag_map.update({None: import_string(default_mapper)})

    return tag_map


def clear_tag_map() -> None:
    """Clear the generated tag map so that it will be re-generated. Useful for tests."""

    global tag_map  # noqa: PLW0603
    tag_map = None
