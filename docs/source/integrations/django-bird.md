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
            ...
            "loaders": [
                (
                    "django.template.loaders.cached.Loader",
                    [
                        "dj_angles.template_loader.Loader",  # required for `dj-angles`
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                    ],
                )
            ],
            "builtins": [
                "django_bird.templatetags.django_bird",  # this is not required, but is useful for `django-bird` and is added by the library's auto settings
            ],
        },
    },
]
```

## Example

```html
<!-- templates/index.html -->
<dj-bird template='button' class='btn'>
  Click me!
</dj-bird>
```

```html+django
<!-- templates/bird/button.html -->
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

```html
<!-- templates/index.html -->
<dj-button class='btn'>
  Click me!
</dj-button>
```

```html+django
<!-- templates/bird/button.html -->
<button {{ attrs }}>
  {{ slot }}
</button>
```
