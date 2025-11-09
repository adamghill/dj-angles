# Inline Expressions

The `dj-angles` approach is shown first and then the equivalent Django Template Language is second.

## `or`

Similar to the [`default` filter](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#default), but feels a little more Pythonic.

```html
{{ request.user.username or request.user.email }}
```

```html
{% if request.user.username %}{{ request.user.username }}{% else %}{{ request.user.email }}{% endif %}
```

## `if`

Python ternary operator where the first part is a conditional, the part after the " if " is the true value, and the part after the " else " is the false value.

```html
{{ request.user.username if request.user.is_authenticated else 'Unknown' }}
```

```html
{% if request.user.is_authenticated %}{{ request.user.username }}{% else %}Unknown{% endif %}
```
