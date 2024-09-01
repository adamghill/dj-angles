<p align="center">
  <h1 align="center">dj-angles &lt;/&gt;</h1>
</p>
<p align="center">Add some more bracket angles to your Django templates</p>

![PyPI](https://img.shields.io/pypi/v/dj-angles?color=blue&style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/dj-angles?color=blue&style=flat-square)
![GitHub Sponsors](https://img.shields.io/github/sponsors/adamghill?color=blue&style=flat-square)

> This code is experimental -- use with caution! Or maybe not at all! 🤷

📦 Package located at https://pypi.org/project/dj-angles/.

## ⭐ Features

- Use HTML-like elements in Django templates, e.g. `<dj-partial />` instead of `{% include 'partial.html' %}`
- Can be sprinkled in as needed, but does not remove existing Django functionality
- Pretend like you are writing React components, but without dealing with JavaScript at all
- Lets you excitedly tell your friends about how neat the Shadow DOM is

## ⚡ Installation

1. Create a new Django project or `cd` to an existing project
1. `pip install dj-angles` to install the `dj-angles` package
1. `Edit settings.py` `TEMPLATES` and add `"dj_angles.template_loader.Loader",` as the first loader. Note: you might need to add the `"loaders"` key since it is not there by default: https://docs.djangoproject.com/en/stable/ref/templates/api/#django.template.loaders.cached.Loader.

```python
TEMPLATES = [
  "BACKEND": "django.template.backends.django.DjangoTemplates",
  # "APP_DIRS": True,  # this cannot be specified if loaders are explicitly set
  "DIRS": [],
  "OPTIONS": {
      "builtins": builtins,
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
]
```

## Example templates

**`base.html`**

```html
<dj-block 'content'>
</dj-block 'content'>
```

**`index.html`**

```html
<dj-extends 'base.html' />  <!-- {% extends 'base.html' %} -->

<dj-block 'content'>  <!-- {% block 'content' %} -->
  <div>
    <h2>Including partials</h2>

    <div>
      <dj-include 'partial.html' />  <!-- {% include 'partial.html' %} -->
    </div>
  </div>

  <dj-verbatim>  <!-- {% verbatim %} -->
    This is verbatim: {% include %}
  </dj-verbatim>  <!-- {% endverbatim %} -->

  <dj-comment>  <!-- {% comment %} -->
    this is a comment
  </dj-comment>  <!-- {% endcomment %} -->

  <dj-#>this is another comment</dj-#>    <!-- {# this is another comment #} -->

  <dj-autoescape-on>  <!-- {% autoescape-on %} -->
    This is escaped
  </dj-autoescape-on>  <!-- {% endautoescape %} -->

  <dj-autoescape-off>  <!-- {% autoescape off %} -->
    This is not escaped
  </dj-autoescape-off>  <!-- {% endautoescape %} -->

  <dj-csrf />  <!-- {% csrf_token %} -->
  
  <dj-debug />  <!-- {% debug %} -->
</dj-block 'content'>  <!-- {% endblock 'content' %} -->
```

**partial.html**

```html
<div style="border: 1px solid red;">
  <p>
    This is a partial: {{ now|date:"c" }}
  </p>
</div>

<style>
  p {
    color: green;
  }
</style>
```

## Include tags

```html
<p>These are all equivalent ways to include partials.</p>

<dj-include 'partial.html' />
<dj-partial />
<$partial />
```

They all compile to the following Django template syntax.

```html
{% include 'partial.html' %}
```

Directories are also supported.

```html
<dj-include 'directory/partial.html' />
<dj-directory/partial />
<$directory/partial />
```

### CSS scoping

To encapsulate component styles, enable the Shadow DOM for the partial. This will ensure that any `style` element in the partial will be contained to that partial.

```html
<p>These are all equivalent ways to include partials.</p>

<dj-include 'partial.html' shadow />
<dj-partial shadow />
<dj-partial! />
<$partial! />
```

They all compile to the following Django template syntax.

```html
<template shadowrootmode='open'>{% include 'partial.html' %}</template>
```

- More details about declaratively creating shadow root: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/template#shadowrootmode
- More details about using the Shadow DOM: https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_shadow_DOM

## Other tags

### `extends`

```html
<dj-extends 'base.html' />
```

```html
{% extends 'base.html' %}
```

### `block`

```html
<dj-block 'content'>
  ...
</dj-block 'content'>
```

```html
{% block 'content' %}
  ...
{% endblock 'content' %}
```

### `verbatim`

```html
<dj-verbatim>
  ...
</dj-verbatim>
```

```html
{% verbatim %}
  ...
{% endverbatim %}
```

### `comment`

```html
<dj-comment>
  ...
</dj-comment>
```

```html
{% comment %}
  ...
{% endcomment %}
```

### `#`

```html
<dj-#>...</dj-#>
```

```html
{# ... #}
```

### `autoescape-on`

```html
<dj-autoescape-on>
  ...
</dj-autoescape-on>
```

```html
{% autoescape on %}
{% endautoescape %}
```

### `autoescape-off`

```html
<dj-autoescape-off>
  ...
</dj-autoescape-off>
```

```html
{% autoescape off %}
{% endautoescape %}
```

### `csrf`, `csrf-token`

```html
<dj-csrf />
```

```html
{% csrf_token %}
```

### `csrf-input`

```html
<dj-csrf-input />
```

```html
<input type='hidden' value='{% csrf_token %}'></input>
```

### `debug`

```html
<dj-debug />
```

```html
{% debug %}
```

### `filter`

```html
<dj-filter ... />
```

```html
{% filter ... %}
```

### `lorem`

```html
<dj-lorem />
```

```html
{% lorem %}
```

### `now`

```html
<dj-now />
```

```html
{% now %}
```

### `spaceless`

```html
<dj-spaceless>
  ...
</dj-spaceless>
```

```html
{% spaceless %}
  ...
{% endspaceless %}
```

### `templatetag`

```html
<dj-templatetag ... />
```

```html
{% templatetag ... %}
```
