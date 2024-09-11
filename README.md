<p align="center">
  <h1 align="center">dj-angles &lt;/&gt;</h1>
</p>
<p align="center">Adds more bracket angles to Django templates</p>

![PyPI](https://img.shields.io/pypi/v/dj-angles?color=blue&style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/dj-angles?color=blue&style=flat-square)
![GitHub Sponsors](https://img.shields.io/github/sponsors/adamghill?color=blue&style=flat-square)

📦 Package located at https://pypi.org/project/dj-angles/.

## ⭐ Features

- Use HTML-like elements in Django templates, e.g. `<dj-partial />` instead of `{% include 'partial.html' %}`
- Can be sprinkled in as needed, but does not remove existing Django functionality
- Pretend like you are writing React components, but without dealing with JavaScript at all
- Lets you excitedly tell your friends how neat the Shadow DOM is
- Since it looks like HTML, syntax highlighting mostly "just works"
- Wraps included templates in a custom element for easier debugging and targeted CSS styling

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

  <dj-image 'img/django.jpg' />  <!-- <img src="{% static 'img/django.jpg' %}" /> -->
  <dj-css 'css/styles.css' />  <!-- <link href="{% static 'css/styles.css' %}" rel="stylesheet" /> -->
</dj-block 'content'>  <!-- {% endblock 'content' %} -->
```

**partial.html**

```html
<div>
  This is a partial: {{ now|date:"c" }}
</div>
```

## ⚡ Installation

1. Create a new Django project or `cd` to an existing project
1. `pip install dj-angles` to install the `dj-angles` package
1. `Edit settings.py` `TEMPLATES` and add `"dj_angles.template_loader.Loader",` as the first loader. Note: you might need to add the `"loaders"` key since it is not there by default (https://docs.djangoproject.com/en/stable/ref/templates/api/#django.template.loaders.cached.Loader) and you will need to remove the `APP_DIRS` setting.

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

## 🪄 Include tags

These are equivalent ways to include partial HTML files.

```html
<dj-include 'partial.html' />
<dj-include 'partial' />
<dj-partial />
```

They all compile to the following Django template.

```html
<dj-partial>{% include 'partial.html' %}</dj-partial>
```

The wrapping `<dj-partial>` element allows for easier debugging when looking at the source code and also allows for targeted CSS styling.

Note: The [other tags](#️-other-tags) are considered reserved words. Template file names that conflict will not get loaded because reserved words take precedence. For example, if there is a template named "extends.html" `<dj-extends />` could not be used to include it; `<dj-include 'extends.html' />` would need to be used instead.

### Appending an identifier to the wrapping element

Adding a colon and an identifier to the end of a template name allows for even more specific CSS styling.

```html
<dj-partial:1 />
```

Would get compiled to the following Django template.

```html
<dj-partial-1>{% include 'partial.html' }</dj-partial-1>
```

### ⤵️ Directories

Accessing templates in directories is supported even though technically forward-slashes [aren't permitted in a custom element](https://html.spec.whatwg.org/multipage/custom-elements.html#valid-custom-element-name). It might confound HTML syntax highlighters.

```html
<dj-include 'directory/partial.html' />
<dj-include 'directory/partial' />
<dj-directory/partial />
```

They all compile to the following Django template.

```html
<dj-directory-partial>{% include 'directory/partial.html' %}</dj-directory-partial>
```

### 🥷 CSS scoping

To encapsulate component styles, enable the Shadow DOM for the partial. This will ensure that any `style` element in the partial will be contained to that partial. The downside is that the Shadow DOM does not allow outside styles in (other than CSS variables).

These are all equivalent ways to include a shadow partial.

```html
<dj-include 'partial.html' shadow />
<dj-partial shadow />
<dj-partial! />
```

They all compile to the following Django template syntax.

```html
<dj-partial><template shadowrootmode='open'>{% include 'partial.html' %}</template></dj-partial>
```

**More information about the Shadow DOM**

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

### `css`

```html
<dj-css 'css/styles.css' />
```

```html
<link href="{% static 'css/styles.css' %}" rel="stylesheet" />
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

### `image`

```html
<dj-image 'img/django.jpg' />
```

```html
<img src="{% static 'img/django.jpg' %}" />
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
# settings.py

ANGLES = {
  "initial_tag_regex": r"(dj-|\$)"
}
```

```html
<dj-include 'partial.html' />
<dj-partial />
<$partial />
```

These would all compile to the following Django template.

```html
{% include 'partial.html' %}
```

#### React-style include

```python
# settings.py

ANGLES = {
  "initial_tag_regex": r"(dj-|(?=[A-Z]))",  # regex matches "dj-" or upper-case letter lookahead
  "lower_case_tag": True,  # without this the template `Partial.html` will be loaded
}
```

```html
<dj-include 'partial.html' />
<dj-partial />
<Partial />
```

These would all compile to the following Django template.

```html
{% include 'partial.html' %}
```

### `lower_case_tag`

Lower-cases the tag. Useful when using [React-style includes](#react-style-include) to convert something like "Partial" to "partial" for the name of the template. `Boolean` which defaults to `False`.

### `mappers`

Provide additional mappers. `Dictionary` which defaults to `{}`.

The key of the dictionary is a string and is the text match of the regex after the `initial_tag_regex`, i.e. for the default `initial_tag_regex` of `r"(dj-)"`, the key would be the result after "dj-" until a space or a ">".

#### string value

When the dictionary value is a string, it replaces the `initial_tag_regex` plus the key, and puts it between "{%" and the arguments plus "%}".

```python
# settings.py

ANGLES = {
    "mappers": {
        "component": "include",
    },
}
```

```html
<dj-component 'partial.html' />
```

Would compile to the following Django template.

```html
{% include 'partial.html' %}
```

#### Callable value

When the dictionary value is a callable, the string result is dictated by the output of the mapper function. The callable has one argument, `Tag`, which encapsulates information about the matched tag that can be useful in building custom functionality, e.g. `component_name`, `is_end`, `is_self_closing`, etc.

```python
# settings.py

from dj_angles import Tag

def map_text(tag: Tag) -> str:
    return "This is some text."

def map_hello(tag: Tag) -> str:
    return f"<p>{tag.component_name.upper()}! {tag.template_tag_args}</p>"

ANGLES = {
    "mappers": {
        "text": map_text,
        "hello": map_hello,
    },
}
```

```html
<dj-text />

<dj-hello 'Goodbye!' />
```

Would compile to the following Django template.

```html
This is some text.

<p>HELLO! Goodbye!</p>
```

## 🤔 How does this work?

The template HTML is passed through `dj_angles.template_loader.Loader` first, tags are matched (via good ole' regex), some transformations happen based on the mappers defined, and then the normal template loaders process the resulting output.

## ✨ Inspiration

I have been interested in Django components and encapsulating functionality for a long time (see [django-unicorn](https://www.django-unicorn.com), [dlitejs](https://dlitejs.com), etc), but had never thought of using HTML directly until I looked at [Cotton](https://django-cotton.com) by [wrabit](https://github.com/wrabit). `dj-angles` takes that idea further to see how well it works.
