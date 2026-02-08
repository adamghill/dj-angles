# django-compressor

> Compresses linked and inline JavaScript or CSS into a single cached file.

- 📖 [https://django-compressor.readthedocs.io/](https://django-compressor.readthedocs.io/)
- 📦 [https://pypi.org/project/django-compressor/](https://pypi.org/project/django-compressor/)
- 🛠️ [https://github.com/django-compressor/django-compressor](https://github.com/django-compressor/django-compressor)

## Installation

Install `django-compressor` and configure it per their documentation. `dj-angles` will automatically detect its presence and enable the `<dj-compress>` tag.

```python
# settings.py

INSTALLED_APPS = [
    ...
    "compressor",
    ...
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]

TEMPLATES = [
    {
        ...
        "OPTIONS": {
            ...
            "builtins": [
                "compressor.templatetags.compress",  # optional for `django-compressor`
            ],
        },
    },
]
```

## Example

### CSS Compression

```html
<!-- Input -->
<dj-compress css>
    <link rel="stylesheet" href="{% static 'css/base.css' %}">
    <style>
        .alert { color: red; }
    </style>
</dj-compress>

<!-- Transformed to -->
{% compress css %}
    <link rel="stylesheet" href="{% static 'css/base.css' %}">
    <style>
        .alert { color: red; }
    </style>
{% endcompress %}
```

### JavaScript Compression

```html
<!-- Input -->
<dj-compress js>
    <script src="{% static 'js/app.js' %}"></script>
</dj-compress>

<!-- Transformed to -->
{% compress js %}
    <script src="{% static 'js/app.js' %}"></script>
{% endcompress %}
```

### Inline Compression

Use the `inline` attribute to embed compressed content directly in the HTML:

```html
<!-- Input -->
<dj-compress css inline>
    <link rel="stylesheet" href="{% static 'css/critical.css' %}">
</dj-compress>

<!-- Transformed to -->
{% compress css inline %}
    <link rel="stylesheet" href="{% static 'css/critical.css' %}">
{% endcompress %}
```

### Preload Mode

```html
<dj-compress css preload>
    <link rel="stylesheet" href="{% static 'css/main.css' %}">
</dj-compress>

<!-- Transformed to -->
{% compress css preload %}
    <link rel="stylesheet" href="{% static 'css/main.css' %}">
{% endcompress %}
```

### Named Blocks

Use the `name` attribute to specify a block name:

```html
<dj-compress css inline name="critical-styles">
    <style>.critical { color: red; }</style>
</dj-compress>

<!-- Transformed to -->
{% compress css inline critical-styles %}
    <style>.critical { color: red; }</style>
{% endcompress %}
```
