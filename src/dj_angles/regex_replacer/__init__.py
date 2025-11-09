import logging

from dj_angles.regex_replacer.attribute_replacer import get_attribute_replacements
from dj_angles.regex_replacer.django_tag_replacer import get_django_tag_replacements
from dj_angles.regex_replacer.tag_replacer import get_tag_replacements

logger = logging.getLogger(__name__)


def convert_template(html: str) -> str:
    """Gets a list of replacements based on template HTML, replaces the necessary strings, and returns the new string.

    Args:
        param html: Template HTML.

    Returns:
        The converted template HTML.
    """

    # Replace dj-angles attributes first
    for replacement in get_attribute_replacements(html=html):
        html = html.replace(
            replacement.original,
            replacement.replacement,
            1,
        )

    # Replace dj-angles django tags second
    for replacement in get_django_tag_replacements(html=html):
        html = html.replace(
            replacement.original,
            replacement.replacement,
            1,
        )

    # Replace dj-angles tags third
    for replacement in get_tag_replacements(html=html):
        html = html.replace(
            replacement.original,
            replacement.replacement,
            1,
        )

    return html
