from dj_angles.mappers.angles import default_mapper, map_angles_include, map_call, map_model
from dj_angles.mappers.django import map_autoescape, map_block, map_css, map_endblock, map_extends, map_image
from dj_angles.mappers.include import map_include
from dj_angles.mappers.thirdparty import map_bird, map_partialdef

__all__ = [
    "default_mapper",
    "map_angles_include",
    "map_autoescape",
    "map_bird",
    "map_block",
    "map_call",
    "map_css",
    "map_endblock",
    "map_extends",
    "map_image",
    "map_include",
    "map_model",
    "map_partialdef",
]
