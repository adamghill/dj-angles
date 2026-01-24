import pytest
from django.conf import settings

from dj_angles.mappers.mapper import clear_tag_map
from dj_angles.templatetags.model import clear_models


def pytest_configure():
    settings.configure(
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "dj_angles",
            "example.book.apps.Config",
        ],
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [
                    "tests/templates",
                ],
                "OPTIONS": {
                    "builtins": [
                        "django_bird.templatetags.django_bird",
                        "dj_angles.templatetags.dj_angles",
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
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
            }
        },
        MIDDLEWARE=(
            "dj_angles.middleware.RequestMethodMiddleware",
            "dj_angles.middleware.RequestAJAXMiddleware",
        ),
        ANGLES={
            "IS_IN_UNIT_TEST": True,
        },
    )


@pytest.fixture(autouse=True)
def reset_settings(settings):
    # Make sure that ANGLES is empty before every test
    settings.ANGLES = {
        "IS_IN_UNIT_TEST": True,
    }

    # Clear the caches before every test
    clear_tag_map()
    clear_models()

    # Run test
    yield
