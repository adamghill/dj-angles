import logging
import re

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

    # 0. Mask comments
    comments = []

    def mask_match(match):
        comments.append(match.group(0))
        return f"__DJ_ANGLES_COMMENT_{len(comments) - 1}__"

    # Django single line comments {# ... #}
    html = re.sub(r"\{#.*?#\}", mask_match, html, flags=re.DOTALL)

    # Django block comments {% comment %}...{% endcomment %}
    html = re.sub(r"\{%\s*comment\s*%\}.*?\{%\s*endcomment\s*%\}", mask_match, html, flags=re.DOTALL | re.IGNORECASE)

    # Custom dj-comment Tags <dj-comment>...</dj-comment>
    html = re.sub(r"<dj-comment>.*?</dj-comment>", mask_match, html, flags=re.DOTALL | re.IGNORECASE)

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
