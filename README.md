<p align="center">
  <h1 align="center">dj-angles &lt;/&gt;</h1>
</p>
<p align="center">Adds more bracket angles to Django templates</p>

![PyPI](https://img.shields.io/pypi/v/dj-angles?color=blue&style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/dj-angles?color=blue&style=flat-square)
![GitHub Sponsors](https://img.shields.io/github/sponsors/adamghill?color=blue&style=flat-square)

> This code is experimental -- use with caution! Or maybe not at all! 🤷

📦 Package located at https://pypi.org/project/dj-angles/.

## ⭐ Features

- Use HTML-like elements in Django templates, e.g. `<dj-partial />` instead of `{% include 'partial.html' %}`
- Can be sprinkled in as needed, but does not remove existing Django functionality
- Pretend like you are writing React components, but without dealing with JavaScript at all
- Lets you excitedly tell your friends how neat the Shadow DOM is
- Since it looks like HTML, syntax highlighting mostly "just works"

## 💥 Example

**`base.html`**

```html
<dj-block 'content'>
</dj-block 'content'>
```

**`index.html`**

```html
<dj-extends 'base.html' />  <!-- {% extends 'base.html' %} -->

<dj-block 'content'>  <!-- {% block 'content' %} -->
  <dj-include 'partial.html' />  <!-- {% include 'partial.html' %} -->

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

## 🪄 Include tags

These are equivalent ways to include partial HTML files.

```html
<dj-include 'partial.html' />
<dj-partial />
```

They both compile to the following Django template syntax.

```html
{% include 'partial.html' %}
```

The [other tags](#️-other-tags) are considered reserved words. Template file names that conflict with the those words won't get loaded because reserved words take precedence. Those would need to use `<dj-include 'partial.html' />` to include the template.

### ⤵️ Directories

Accessing templates in directories is supported even though technically forward-slashes [aren't permitted in a custom element](https://html.spec.whatwg.org/multipage/custom-elements.html#valid-custom-element-name). It will definitely confound most HTML syntax highlighters.

```html
<dj-include 'directory/partial.html' />
<dj-directory/partial />
```

### 🥷 CSS scoping

To encapsulate component styles, enable the Shadow DOM for the partial. This will ensure that any `style` element in the partial will be contained to that partial. The downside is that the Shadow DOM does not allow outside styles in, other than CSS variables.

These are all equivalent ways to include partials.

```html
<dj-include 'partial.html' shadow />
<dj-partial shadow />
<dj-partial! />
```

They all compile to the following Django template syntax.

```html
<template shadowrootmode='open'>{% include 'partial.html' %}</template>
```

- Shadow DOM styling: https://javascript.info/shadow-dom-style
- Declaratively creating a shadow root: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/template#shadowrootmode
- Using the Shadow DOM: https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_shadow_DOM

## 🛠️ Other tags

### [`#`](https://docs.djangoproject.com/en/stable/ref/templates/language/#comments)

```html
<dj-#>...</dj-#>
```

```html
{# ... #}
```

### [`autoescape-off`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#autoescape)

```html
<dj-autoescape-off>
  ...
</dj-autoescape-off>
```

```html
{% autoescape off %}
{% endautoescape %}
```

### [`autoescape-on`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#autoescape)

```html
<dj-autoescape-on>
  ...
</dj-autoescape-on>
```

```html
{% autoescape on %}
{% endautoescape %}
```

### [`block`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#block)

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

### [`csrf`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#csrf-token), [`csrf-token`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#csrf-token), [`csrf-input`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#csrf-token)

```html
<dj-csrf />
```

```html
{% csrf_token %}
```

### [`comment`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#comment)

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

### [`debug`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#debug)

```html
<dj-debug />
```

```html
{% debug %}
```

### [`extends`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#extends)

```html
<dj-extends 'base.html' />
```

```html
{% extends 'base.html' %}
```

### [`filter`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#filter)

```html
<dj-filter ... />
```

```html
{% filter ... %}
```

### [`lorem`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#lorem)

```html
<dj-lorem />
```

```html
{% lorem %}
```

### [`now`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#now)

```html
<dj-now />
```

```html
{% now %}
```

### [`spaceless`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#spaceless)

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

### [`templatetag`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#templatetag)

```html
<dj-templatetag ... />
```

```html
{% templatetag ... %}
```

### [`verbatim`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#verbatim)

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

## Settings

Settings can be configured via an `ANGLES` dictionary in `settings.py`.

```python
ANGLES = {}
```

### `initial_tag_regex`

Determines the characters that are used to indicate a `dj-angles` element. `String` which defaults to `r"(dj-)"`.

#### Special character

```python
ANGLES = {
  "initial_tag_regex": r"(dj-|\$)"
}
```

```html
<dj-partial />
<$partial />
```

```html
{% include 'partial.html' %}
```

#### Regular element

```python
ANGLES = {
  "initial_tag_regex": ""
}
```

```html
<partial />
```

```html
{% include 'partial.html' %}
```

#### React-like component

```python
ANGLES = {
  "initial_tag_regex": "",
  "lower_case_tag": True
}
```

```html
<Partial />
```

```html
{% include 'partial.html' %}
```

### `lower_case_tag`

Lower-cases the tag. `Boolean` which defaults to `False`.

### `mappers`

Provide additional mappers. `Dictionary` which defaults to `{}`.

The key is always a string and is the regex match after the `initial_tag_regex`, i.e. for the default `initial_tag_regex` of `r"(dj-)"`, the key would match after "dj-" until a space or a `>`.

#### string value

When the dictionary value is a string, it replaces the `initial_tag_regex` + the key, and puts it into a template tag.

```python
# settings.py

ANGLES = {
    "mappers": {
        "blob": "include",
    },
}
```

```html
<dj-blob 'partial.html' />
```

```html
{% include 'partial.html' %}
```

#### Callable

When the dictionary value is a callable, the output can be completely controlled.

```python
# settings.py

def map_blob(component_name, template_tag_args, is_tag_closing):
    return "blob2"

ANGLES = {
    "mappers": {
        "blob": map_blob,
    },
}
```

```html
<dj-blob />
```

```html
blob2
```

## 🤔 How does this work?

Basically, Django template loaders are super powerful. The raw template content is passed through `dj_angles.template_loader.Loader` first, some transformations happen (via good ole' regex), and then the normal template loaders process the output like normal.

## ✨ Inspiration

I have been interested in Django components and encapsulating functionality for a long time (see [django-unicorn](https://www.django-unicorn.com), [dlitejs](https://dlitejs.com), etc), but had never thought of using HTML directly until I looked at [Cotton](https://django-cotton.com) by [wrabit](https://github.com/wrabit).

💡

Since `<c-component />` is a high-powered wrapper around `{% include %}`, what if other Django templatetags could also be wrapped? This library is an experiment to see what that experience is like and how well it works.
