import logging

from dj_angles.replacers.attributes import replace_attributes
from dj_angles.replacers.comments import mask_comments
from dj_angles.replacers.tags import replace_tags
from dj_angles.replacers.variables import replace_variables
from dj_angles.settings import get_setting

logger = logging.getLogger(__name__)


def convert_template(html: str, *, origin=None) -> str:
    """Convert a dj-angles template string to Django template syntax.

    Args:
        html: The template HTML string to convert.
        origin: The origin of the template.

    Returns:
        The converted template HTML string.
    """

    # 0. Mask comments
    initial_tag_regex = get_setting("initial_tag_regex", default=r"(dj-)")

    (html, comments) = mask_comments(html, initial_tag_regex=initial_tag_regex)

    # 1. Replace attributes, e.g. `<div dj-if="condition">`
    html = replace_attributes(html)

    # 2. Replace variables, e.g. `{{ foo or bar }}`
    html = replace_variables(html)

    # 3. Replace tags, e.g. `<dj-include />`
    html = replace_tags(html, origin=origin)

    # 4. Unmask comments
    for i, comment in enumerate(comments):
        html = html.replace(f"__DJ_ANGLES_COMMENT_{i}__", comment)

    return html
