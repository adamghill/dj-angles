# django-template-partials

>Reusable named inline partials for the Django Template Language.

- 📦 [https://pypi.org/project/django-template-partials/](https://pypi.org/project/django-template-partials/)
- 🛠️ [https://github.com/carltongibson/django-template-partials](https://github.com/carltongibson/django-template-partials)

## Installation

Using the auto settings of  `django-template-partials` will conflict with `dj-angles`. You will need to install it using the [advanced configuration](https://github.com/carltongibson/django-template-partials#advanced-configuration).

```python
# settings.py

INSTALLED_APPS = {
    ...
    "template_partials.apps.SimpleAppConfig",
    ...
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "OPTIONS": {
            "context_processors": [
                ...
            ],
            "loaders": [
                (
                    "template_partials.loader.Loader",
                    [
                        (
                            "django.template.loaders.cached.Loader",
                            [
                                "dj_angles.template_loader.Loader",
                                "django.template.loaders.filesystem.Loader",
                                "django.template.loaders.app_directories.Loader",
                            ],
                        )
                    ],
                )
            ],
            "builtins": [
                ...
                "template_partials.templatetags.partials",
                ...
            ],
        },
    },
]
```

## Example

```html
<dj-partial name="test-partial">
  TEST-PARTIAL-CONTENT
</dj-partial>
```

is equivalent to:

```html
{% partialdef test-partial %}
  TEST-PARTIAL-CONTENT
{% endpartialdef %}
```
