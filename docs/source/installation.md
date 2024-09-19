# Installation

1. Create a new Django project or `cd` to an existing project
1. `pip install dj-angles`
1. Edit `TEMPLATES` in `settings.py` and add `"dj_angles.template_loader.Loader",` as the first loader. Note: you might need to add the `"loaders"` key since it is not there by default (https://docs.djangoproject.com/en/stable/ref/templates/api/#django.template.loaders.cached.Loader). Also remove the `APP_DIRS` setting.

```python
# settings.py

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
