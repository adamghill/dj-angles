# Attributes

The `dj-angles` approach is shown first and then the equivalent Django Template Language is second.

## [`if`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#if)

```html
<div dj-if="True">...</div>
```

```html
{% if True %}<div>...</div>{% endif %}
```

## [`elif`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#if)

```html
<div dj-if="some_list.0">
  if
</div>
<div dj-elif="some_list.1">
  elif
</div>
```

```html
{% if some_list.0 %}
<div>
  if
</div>
{% elif some_list.1 %}
<div>
  elif
</div>
{% endif %}
```

## [`else`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#if)

```html
<div dj-if="some_variable == 1">
  if
</div>
<div dj-elif="some_variable == 2">
  elif
</div>
<div dj-else>
  else
</div>
```

```html
{% if some_variable == 1 %}
<div>
  if
</div>
{% elif some_variable == 2 %}
<div>
  elif
</div>
{% else %}
<div>
  else
</div>
{% endif %}
```