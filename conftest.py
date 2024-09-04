from django.conf import settings


def pytest_configure():
    settings.configure(
        SECRET_KEY="this-is-a-secret",
        ANGLES={},
    )
