# django-bird

>High-flying components for perfectionists with deadlines.

- 📖 [https://django-bird.readthedocs.io/](https://django-bird.readthedocs.io/)
- 📦 [https://pypi.org/project/django-bird/](https://pypi.org/project/django-bird/)
- 🛠️ [https://github.com/joshuadavidthomas/django-bird](https://github.com/joshuadavidthomas/django-bird)

## Installation

Using the auto settings `django-bird` should not conflict with the two packages. If you would like to configure the library manually here is an example. See [https://django-bird.readthedocs.io/en/latest/configuration.html#manual-setup](https://django-bird.readthedocs.io/en/latest/configuration.html#manual-setup) for more details.

```{note}
`django-bird` deprecated its custom template loader in [v0.13.0](https://github.com/joshuadavidthomas/django-bird/releases/tag/v0.13.0), so if you are on an older version you will need to update to use the example config below.
```

```python
# settings.py


DJANGO_BIRD = {
    "ENABLE_AUTO_CONFIG": False
}  # this is optional for `django-bird`

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",  # this allows `django-bird` to find components
        ],
        "OPTIONS": {
            "builtins": [
                "django_bird.templatetags.django_bird",  # this is not required, but is useful for `django-bird` and is added by the library's auto settings
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
