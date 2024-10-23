import pytest
from django.conf import settings

from dj_angles.regex_replacer import clear_tag_map


def pytest_configure():
    settings.configure(
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [
                    "tests/templates",
                ],
                "OPTIONS": {
                    "builtins": [
                        "django_bird.templatetags.django_bird",
                    ],
                    "context_processors": [
                        "django.template.context_processors.debug",
                        "django.template.context_processors.request",
                        "django.contrib.auth.context_processors.auth",
                        "django.contrib.messages.context_processors.messages",
                    ],
                    "loaders": [
                        (
                            "django.template.loaders.cached.Loader",
                            [
                                "dj_angles.template_loader.Loader",
                                "django_bird.loader.BirdLoader",
                                "django.template.loaders.filesystem.Loader",
                                "django.template.loaders.app_directories.Loader",
                            ],
                        )
                    ],
                },
            },
        ],
        SECRET_KEY="this-is-a-secret",
        ANGLES={},
    )


@pytest.fixture(autouse=True)
def reset_settings(settings):
    # Make sure that ANGLES is empty before every test
    settings.ANGLES = {}

    # Clear the tag map before every test
    clear_tag_map()

    # Run test
    yield
