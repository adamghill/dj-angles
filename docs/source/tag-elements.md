# Tags

The `dj-angles` approach is shown first and then the equivalent Django Template Language is second.

## [`#`](https://docs.djangoproject.com/en/stable/ref/templates/language/#comments)

```
<dj-#>...</dj-#>
```

```html
{# ... #}
```

## [`autoescape-off`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#autoescape)

```html
<dj-autoescape-off>
  ...
</dj-autoescape-off>
```

```html
{% autoescape off %}
{% endautoescape %}
```

## [`autoescape-on`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#autoescape)

```html
<dj-autoescape-on>
  ...
</dj-autoescape-on>
```

```html
{% autoescape on %}
{% endautoescape %}
```

## [`block`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#block)

```
<dj-block name='content'>
  ...
</dj-block>
```

```{note}
The end tag can optionally have a name attribute. If it is missing, the `endblock` will use the name attribute from the start tag.
```

```
<dj-block name='content'>
  ...
</dj-block name='content'>
```

```{note}
The tag can be self-closing if there is not default block content.
```

```
<dj-block name='content' />
```

```html
{% block content %}
  ...
{% endblock content %}
```

## [`call`](template-tags/call.md)

```
<dj-call code='slugify("Hello Goodbye")' as='variable_name' />
```

```html
{% call slugify("Hello Goodbye") as variable_name %}
```

## [`csrf`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#csrf-token), [`csrf-token`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#csrf-token), [`csrf-input`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#csrf-token)

```html
<dj-csrf />
```

```html
{% csrf_token %}
```

## [`comment`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#comment)

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

## `css`

```
<dj-css href='css/styles.css' />
```

```html
<link href="{% static 'css/styles.css' %}" rel="stylesheet" />
```

## [`debug`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#debug)

```html
<dj-debug />
```

```html
{% debug %}
```

## [`extends`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#extends)

```
<dj-extends parent='base' />
<dj-extends parent='base.html' />
```

```html
{% extends 'base.html' %}
```

## [`filter`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#filter)

```
<dj-filter ... />
```

```html
{% filter ... %}
```

## [`lorem`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#lorem)

```html
<dj-lorem />
```

```html
{% lorem %}
```

## `image`

```
<dj-image src='img/django.jpg' />
```

```html
<img src="{% static 'img/django.jpg' %}" />
```

## [`model`](template-tags/model.md)

```
<dj-model code='Book.objects.filter(id=1)' as='book' />
```

```html
{% model Book.objects.filter(id=1) as book %}
```

## [`now`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#now)

```html
<dj-now />
```

```html
{% now %}
```

## [`spaceless`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#spaceless)

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

## [`templatetag`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#templatetag)

```
<dj-templatetag ... />
```

```html
{% templatetag ... %}
```

## [`verbatim`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#verbatim)

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