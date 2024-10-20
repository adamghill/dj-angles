from django.conf import settings


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
