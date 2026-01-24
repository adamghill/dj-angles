# django-components

> Create simple reusable template components in Django

- 📖 [https://django-components.github.io/django-components](https://django-components.github.io/django-components)
- 📦 [https://pypi.org/project/django-components/](https://pypi.org/project/django-components/)
- 🛠️ [https://github.com/django-components/django-components](https://github.com/django-components/django-components)

## Installation

Install `django-components` and configure it per their documentation. The libraries work together with proper loader configuration:

```python
# settings.py

INSTALLED_APPS = [
    ...
    "django_components",
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
                        "django_components.template_loader.Loader",  # required for`django-components`
                    ],
                )
            ],
            "builtins": [
                "django_components.templatetags.component_tags",  # required for `django-components`
            ],
        },
    },
]
```

## Example

First, define a component in Python:

```python
# components/calendar/calendar.py
from django_components import Component, register

@register("calendar")
class Calendar(Component):
    template = """
    <div class="calendar">
        <span>{{ date }}</span>
    </div>
    """
    
    css = """
    .calendar {
        background: pink;
    }
    """
```

Then, use it in templates with `dj-angles` syntax:

```html
<!-- Input -->
<dj-component name="calendar" date="2025-01-22">
</dj-component>

<!-- Transformed to -->
{% component 'calendar' date="2025-01-22" %}
{% endcomponent %}
```

## Self-Closing Tags

```html
<dj-component name="icon" type="star" />
```

Transforms to:

```html
{% component 'icon' type="star" / %}
```

## With Slots

Django-components supports slots for nested content:

```html
<dj-component name="card">
    <h1>Title</h1>
    <p>Content here</p>
</dj-component>
```
