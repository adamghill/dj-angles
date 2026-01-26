# django-viewcomponent

> Build reusable components in Django, inspired by Rails ViewComponent

- 📖 [https://django-viewcomponent.readthedocs.io](https://django-viewcomponent.readthedocs.io)
- 📦 [https://pypi.org/project/django-viewcomponent/](https://pypi.org/project/django-viewcomponent/)
- 🛠️ [https://github.com/rails-inspire-django/django-viewcomponent](https://github.com/rails-inspire-django/django-viewcomponent)

## Installation

Install `django-viewcomponent` and configure it per their documentation. The libraries work together with proper loader configuration:

```python
# settings.py

INSTALLED_APPS = [
    ...
    "django_viewcomponent",
    ...
]

TEMPLATES = [
    {
        ...
        "OPTIONS": {
            ...
            "loaders": [
                (
                    "django.template.loaders.cached.Loader",
                    [
                        "dj_angles.template_loader.Loader",  # required for `dj-angles`
                        "django.template.loaders.filesystem.Loader",  # default Django loader
                        "django.template.loaders.app_directories.Loader",  # same as APP_DIRS=True
                        "django_viewcomponent.loaders.ComponentLoader",  # required for`django-viewcomponent
                    ],
                )
            ],
            "builtins": [
                "django_viewcomponent.templatetags.viewcomponent_tags",  # optional for `django-viewcomponent`
            ],
        },
    },
]
```

## Example

First, define a component in Python:

```python
# components/example/example.py
from django_viewcomponent import component


@component.register("example")
class ExampleComponent(component.Component):
    template_name = "example/example.html"

    def __init__(self, **kwargs):
        self.title = kwargs['title']
```

Then, use it in templates with `dj-angles` syntax:

```html
<!-- Input -->
<dj-viewcomponent name="example" title="Example"></dj-viewcomponent>

<!-- Transformed to -->
{% component 'example' title="Example" %}{% endcomponent %}
```

## Self-Closing Tags

```html
<dj-viewcomponent name="example" title="Example" />
```

Transforms to:

```html
{% component 'example' title="Example" %}{% endcomponent %}
```

## With Slots

django-viewcomponent supports slots for nested content:

```html
<dj-viewcomponent name="card">
    <h1>Title</h1>
    <p>Content here</p>
</dj-viewcomponent>
```
