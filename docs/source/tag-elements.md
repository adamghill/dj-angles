# Tags

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
<dj-block 'content'>
  ...
</dj-block 'content'>
```

```html
{% block 'content' %}
  ...
{% endblock 'content' %}
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
<dj-css 'css/styles.css' />
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
<dj-extends 'base.html' />
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
<dj-image 'img/django.jpg' />
```

```html
<img src="{% static 'img/django.jpg' %}" />
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