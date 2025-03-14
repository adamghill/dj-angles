# Installation

1. Create a new Django project or `cd` to an existing project
1. `pip install dj-angles`
1. Edit `TEMPLATES` in `settings.py` and add `"dj_angles.template_loader.Loader",` as the first loader. Note: you might need to add the `"loaders"` key since it is not there by default (https://docs.djangoproject.com/en/stable/ref/templates/api/#django.template.loaders.cached.Loader). Also remove the `APP_DIRS` setting.

```python
# settings.py

...
TEMPLATES = [{
  "BACKEND": "django.template.backends.django.DjangoTemplates",
  # "APP_DIRS": True,  # this cannot be specified if OPTIONS.loaders is explicitly set
  "DIRS": [],
  "OPTIONS": {
      "context_processors": [
          "django.template.context_processors.request",
          "django.template.context_processors.debug",
          "django.template.context_processors.static",
      ],
      "loaders": [
          (
              "django.template.loaders.cached.Loader",
              [
                  "dj_angles.template_loader.Loader",  # this is required for `dj-angles`
                  "django.template.loaders.filesystem.Loader",
                  "django.template.loaders.app_directories.Loader",
              ],
          )
      ],
  },
}]
```

## Template Tags

`dj-angles` includes regular Django template tags that can be used even if not using the `dj-angles` template loader. However, it must be registered so the template tags can be found.

```python
# settings.py

...
INSTALLED_APPS = [
    ...
    "dj_angles",
]
```

They can loaded in any template using the `{% load dj_angles %}` tag. Or they can be added to `builtins` which makes them available in all templates automatically.

```python
# settings.py

...
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "OPTIONS": {
            ...
            "builtins": [
                "dj_angles.templatetags.dj_angles",
            ],
        },
    },
]
```
