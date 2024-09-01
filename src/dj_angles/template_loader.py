import os
import re

from django.apps import apps
from django.template import TemplateDoesNotExist
from django.template.loaders.app_directories import Loader as AppDirectoriesLoader

from dj_angles.mappers import HTML_TAG_TO_DJANGO_TEMPLATE_TAG_MAP

# TODO: Base this on settings?
INITIAL_TAG_CHARACTERS = r"(dj-|\$)"
TAG_REGEX = rf"</?({INITIAL_TAG_CHARACTERS}(?P<component_name>[^\s>]+))\s*(?P<template_tag_args>.*?)\s*/?>"
TAG_RE = re.compile(TAG_REGEX)


def get_include_replacement(template_name: str, *, is_shadow: bool = False, is_tag_self_closing: bool = False) -> str:
    template_name = template_name.strip()

    if "." in template_name:
        template_file = f"'{template_name}'"
    else:
        template_file = f"'{template_name}.html'"

    if (template_name.startswith("'") and template_name.endswith("'")) or (
        template_name.startswith('"') and template_name.endswith('"')
    ):
        template_file = template_file[1:-1]

    replacement = f"{{% include {template_file} %}}"

    if is_shadow:
        replacement = f"<template shadowrootmode='open'>{{% include {template_file} %}}"

        if is_tag_self_closing:
            replacement = f"{replacement}</template>"

    return replacement


def get_replacements(template_string: str) -> list:
    replacements = []
    last_open_component_name = None

    for match in re.finditer(TAG_RE, template_string):
        original = template_string[match.start() : match.end()]
        component_name = match.group("component_name")

        if last_open_component_name:
            if component_name.endswith("!"):
                if last_open_component_name != component_name[:-1]:
                    raise AssertionError(f"Expected closing tag for {component_name[:-1]}")
            elif last_open_component_name != component_name:
                raise AssertionError(f"Expected closing tag for {component_name}")

            last_open_component_name = None

        replacement = None
        is_tag_closing = original.startswith("</")
        is_tag_self_closing = original.endswith("/>")

        if django_template_tag := HTML_TAG_TO_DJANGO_TEMPLATE_TAG_MAP.get(component_name):
            # Get a string of the rest of the match after the component name
            # TODO: Parse this string to be able to handle more complicated cases?
            template_tag_args: str = match.group("template_tag_args") if len(match.groups()) > 2 else ""

            is_django_template_tag_callable = callable(django_template_tag)

            # Handle end tags
            if is_tag_closing and not is_django_template_tag_callable:
                django_template_tag = f"end{django_template_tag}"

            if is_django_template_tag_callable:
                replacement = django_template_tag(
                    component_name=component_name, template_tag_args=template_tag_args, is_tag_closing=is_tag_closing
                )
            elif django_template_tag == "include":
                is_shadow = False

                if template_tag_args and "shadow" in template_tag_args:
                    # Remove shadow from the arg if needed
                    template_tag_args = template_tag_args.replace("shadow", "")
                    is_shadow = True

                if not template_tag_args:
                    raise AssertionError("{% include %} must have an template name")

                replacement = get_include_replacement(
                    template_name=template_tag_args, is_shadow=is_shadow, is_tag_self_closing=is_tag_self_closing
                )
            elif template_tag_args:
                replacement = f"{{% {django_template_tag} {template_tag_args} %}}"
            else:
                replacement = f"{{% {django_template_tag} %}}"
        elif original.startswith("</"):
            replacement = "</template>"
        else:
            # Handle `include` shorthand, e.g. `<dj-partial />`
            is_shadow = len(match.groups()) > 2 and match.group("template_tag_args") == "shadow"

            if component_name.endswith("!"):
                # Handle shadow shorthand
                component_name = component_name[:-1]
                is_shadow = True

            if not is_tag_self_closing:
                last_open_component_name = component_name

            replacement = get_include_replacement(
                template_name=component_name, is_shadow=is_shadow, is_tag_self_closing=is_tag_self_closing
            )

        if replacement:
            replacements.append((original, replacement))

    return replacements


def replace_strings(template_string: str) -> str:
    replacements = get_replacements(template_string=template_string)

    for r in replacements:
        template_string = template_string.replace(
            r[0],
            r[1],
        )

    return template_string


class Loader(AppDirectoriesLoader):
    def get_contents(self, origin):
        template_string = self._get_template_string(origin.name)
        template_string = replace_strings(template_string)

        return template_string

    def _get_template_string(self, template_name):
        try:
            with open(template_name, encoding=self.engine.file_charset) as f:
                return f.read()
        except FileNotFoundError as e:
            raise TemplateDoesNotExist(template_name) from e

    def get_dirs(self):
        """This works like the file loader with APP_DIRS = True.

        Swiped from https://github.com/wrabit/django-cotton/blob/ab1a98052de48266c62ff226ab0ec85b89d038b6/django_cotton/cotton_loader.py#L59.
        """

        dirs = self.engine.dirs

        for app_config in apps.get_app_configs():
            template_dir = os.path.join(app_config.path, "templates")

            if os.path.isdir(template_dir):
                dirs.append(template_dir)

        return dirs
