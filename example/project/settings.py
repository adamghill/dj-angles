from pathlib import Path

from dj_angles import get_template_loaders

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "django-insecure-x#vt_3aic#cyvkwell%zb$wfr5yx-^2=mq-_ei2qo!g1$s#_1t"
DEBUG = True

ALLOWED_HOSTS: list[str] = [
    "0.0.0.0",  # noqa: S104
    "localhost",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "www",
    "dj_angles",
    "django_bird",
    "django_components",
    "django_viewcomponent",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

ANGLES = {
    "slots_enabled": True,
    # "initial_tag_regex": r"(?=\w)",
    # "map_explicit_tags_only": True,
    # "default_mapper": None,
    "mappers": {
        "template": "dj_angles.mappers.map_include",
    },
    "error_boundaries": {"enabled": True, "shadow": True},
}
DJANGO_BIRD = {"ENABLE_AUTO_CONFIG": False}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "OPTIONS": {
            "builtins": [
                "dj_angles.templatetags.dj_angles",
            ],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": get_template_loaders(),
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
