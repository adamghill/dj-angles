DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
SECRET_KEY = "not-a-real-secret"
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "dj_angles",
    "tests",
]
ROOT_URLCONF = "tests.dj_angles.templatetags.view.test_urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
            ],
        },
    },
]
