import logging

from dj_angles.replacers.attributes import replace_attributes
from dj_angles.replacers.tags import replace_tags
from dj_angles.replacers.variables import replace_variables

logger = logging.getLogger(__name__)


def convert_template(html: str, *, origin=None) -> str:
    """Convert a dj-angles template string to Django template syntax.

    Args:
        html: The template HTML string to convert.
        origin: The origin of the template.

    Returns:
        The converted template HTML string.
    """

    # 1. Replace attributes, e.g. `<div dj-if="condition">`
    html = replace_attributes(html)

    # 2. Replace variables, e.g. `{{ foo or bar }}`
    html = replace_variables(html)

    # 3. Replace tags, e.g. `<dj-include />`
    html = replace_tags(html, origin=origin)

    return html
