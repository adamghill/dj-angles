import os

from django.apps import apps
from django.template import TemplateDoesNotExist
from django.template.loaders.app_directories import Loader as AppDirectoriesLoader

from dj_angles.replacers import convert_template


class Loader(AppDirectoriesLoader):
    def _get_template_string(self, template_name):
        """Get the string content as a template."""

        try:
            with open(template_name, encoding=self.engine.file_charset) as f:
                return f.read()
        except FileNotFoundError as e:
            raise TemplateDoesNotExist(template_name) from e

    def get_contents(self, origin) -> str:
        """Gets the converted template contents."""

        template_string = self._get_template_string(origin.name)
<<<<<<< HEAD
        converted_template_string = convert_template(template_string)
=======
        converted_template_string = replace_django_template_tags(template_string, origin=origin)
>>>>>>> b8109bf (Remove support for boundary from includes, add new tag and add support to blocks.)

        return converted_template_string

    def get_dirs(self):
        """Gets the template directories. This works like the file loader with `APP_DIRS = True`.

        From https://github.com/wrabit/django-cotton/blob/ab1a98052de48266c62ff226ab0ec85b89d038b6/django_cotton/cotton_loader.py#L59.
        """

        dirs = self.engine.dirs

        for app_config in apps.get_app_configs():
            template_dir = os.path.join(app_config.path, "templates")

            if os.path.isdir(template_dir):
                dirs.append(template_dir)

        return dirs
