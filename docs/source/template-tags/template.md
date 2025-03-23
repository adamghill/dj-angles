# template

The `template` template tag allows inline templates to be stored and then rendered.

```{note}
Make sure to [install `dj_angles`](../installation.md#template-tags) and include `{% load dj_angles %}` in your template if `"dj_angles.templatetags.dj_angles"` is not added to template built-ins.
```

## Example

```html
{% template field(name, value='') %}
<input name="{{ name }}" value="{{ value }}" />
{% endtemplate %}

{% call field('first-name') %}
<!-- 
<input name="first-name" value="" />
-->

{% call field('last-name', value='Smith') %}
<!-- 
<input name="last-name" value="Smith" />
-->
```

## Creating the template

The `template` looks like a regular Python function. The name of the function will be used to "call" it later to render the function. The arguments are passed to the function when it is called -- both args and kwargs are supported.

````{warning}
There is not support for passing in an arg that would fallback to a kwarg. The number of arguments passed in to a `call` must be the same number of arguments defined in the `template`.

```html
<!-- this works -->
{% template field(name, value='') %}
...
{% endtemplate %}

{% call field('first-name') %}
```

```html
<!-- this works -->
{% template field(name='', value='') %}
...
{% endtemplate %}

{% call field(name='first-name') %}
```

```html
<!-- this does NOT work -->
{% template field(name='', value='') %}
...
{% endtemplate %}

{% call field('first-name') %}
```
````

### Template variables

Template variables will get resolved as expected when calling the template.

```python
# views.py
from django.shortcuts import render

def index(request):
    return render(request, 'index.html', {'field_name': 'surname'})
```

```html
{% template field(name) %}
<input name="{{ name }}" />
{% endtemplate %}

{% call field(field_name) %}
<!-- 
<input name="surname" />
-->
```

### Context

By default the overall context can not be used inside the `template` template tag.

```python
# views.py
from django.shortcuts import render

def index(request):
    return render(request, 'index.html', {'field_name': 'surname'})
```

```html
<!-- index.html -->
{% template field() %}
<input name="{{ field_name }}" />
{% endtemplate %}

{% call field() %}
<!-- 
<input name="" />
-->
```

If you need to pass the context to the template, add `with context` after the function.

```python
# views.py
from django.shortcuts import render

def index(request):
    return render(request, 'index.html', {'field_name': 'surname'})
```

```html
<!-- index.html -->
{% template field() with context %}
<input name="{{ field_name }}" />
{% endtemplate %}

{% call field() %}
<!-- 
<input name="surname" />
-->
```

## How does this work?

The `template` template tag is a [custom template tag](https://docs.djangoproject.com/en/stable/howto/custom-template-tags/#advanced-custom-template-tags) which parses the first argument into Python AST. It then grabs the rest of the template until the `endtemplate` tag is reached as a `NodeList`. It then passes the parsed function and the `NodeList` to the [`call` template tag](call.md) which knows how to render the `NodeList`.

## Other approaches

- https://github.com/carltongibson/django-template-partials
