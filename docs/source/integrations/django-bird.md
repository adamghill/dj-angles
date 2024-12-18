# django-bird

>High-flying components for perfectionists with deadlines.

- 📖 [https://django-bird.readthedocs.io/](https://django-bird.readthedocs.io/)
- 📦 [https://pypi.org/project/django-bird/](https://pypi.org/project/django-bird/)
- 🛠️ [https://github.com/joshuadavidthomas/django-bird](https://github.com/joshuadavidthomas/django-bird)

## Installation

Using the auto settings in `django-bird` will unfortunately create a conflict with the two packages, so the settings must done manually. Here is an example, but see https://django-bird.readthedocs.io/en/latest/configuration.html#manual-setup for more details.

```python
# settings.py


DJANGO_BIRD = {
    "ENABLE_AUTO_CONFIG": False
}  # this is required for `django-bird`

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",  # this allows `django-bird` to find components
        ],
        "OPTIONS": {
            "builtins": [
                "django_bird.templatetags.django_bird",  # this is not required, but is useful for `django-bird`
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
                        "dj_angles.template_loader.Loader",  # this is required for to be first for `dj-angles`
                        "django_bird.loader.BirdLoader",  # this is required for `django-bird`
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                    ],
                )
            ],
        },
    },
]
```

## Example

**templates/index.html**

```html
<dj-bird template='button' class='btn'>
  Click me!
</dj-bird>
```

**templates/bird/button.html**

```
<button {{ attrs }}>
  {{ slot }}
</button>
```

### Default mapper

Setting [`default_mapper`](../settings.md#default_mapper) provides even tighter integration with `django-bird`. `dj-angles` will use `django-bird` for any tag name that it does not have a mapper for (instead of the default `include` template tag.

```python
# settings.py
ANGLES = {
    "default_mapper": "dj_angles.mappers.thirdparty.map_bird",
}
```

**templates/index.html**

```html
<dj-button class='btn'>
  Click me!
</dj-button>
```

**templates/bird/button.html**

```
<button {{ attrs }}>
  {{ slot }}
</button>
```
