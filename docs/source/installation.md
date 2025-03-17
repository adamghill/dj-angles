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

`dj-angles` includes regular Django template tags that can be used even if not using the `dj-angles` template loader.

```python
# settings.py

...
INSTALLED_APPS = [
    ...
    "dj_angles",
]
```

They can be loaded in any template by using `{% load dj_angles %}`. Or `"dj_angles.templatetags.dj_angles"` can be added to template built-ins in `settings.py` to make them available in all templates automatically.

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

## Middleware

`dj-angles` includes middleware for checking the request method and whether the request is AJAX.

```python
# settings.py

...
MIDDLEWARE = [
    ...
    "dj_angles.middleware.RequestMethodMiddleware",
    "dj_angles.middleware.RequestAJAXMiddleware",
]
```

## Scripts

Add scripts for custom elements.

```html
<!-- base.html -->
{% load dj_angles %}

{% dj_angles_scripts %}
```
