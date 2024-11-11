from typing import Optional

from django.template import Template
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import select_template

from dj_angles.strings import dequotify


def get_template(template_file: str) -> Optional[Template]:
    """Check for the template file by looking for different template file variations.

    Currently, the only other variation is looking for the template file with an underscore
    in front (a typical convention for partials).

    Args:
        param template_file: The original template file name.

    Returns:
        A constructed template object for the template file or `None` if it cannot be found.
    """

    template = None

    template_file = dequotify(template_file)
    template_file_list = [template_file]

    if not template_file.startswith("_"):
        if "/" in template_file:
            # Grab the last part and prepend an underscore to it, then reassemble the path
            # TODO: Maybe a better way to do this with pathlib or something OS-agnostic
            template_pieces = template_file.split("/")
            file_name = template_pieces.pop(-1)
            template_pieces.append(f"_{file_name}")
            template_file = "/".join(template_pieces)

            template_file_list.append(template_file)
        else:
            template_file_list.append(f"_{template_file}")

    try:
        template = select_template(template_file_list)
    except TemplateDoesNotExist:
        pass

    return template
