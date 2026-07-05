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

## `value`

```html
<div dj-value="request.user"></div>
```

```html
<div>{{ request.user }}</div>
```

`dj-value` replaces the element's inner content with the value wrapped in `{{ }}`. It can be combined with `dj-if` to conditionally render a value:

```html
<div dj-if="is_authenticated" dj-value="request.user"></div>
```

```html
{% if is_authenticated %}<div>{{ request.user }}</div>{% endif %}
```

Filters and expressions are passed through as-is:

```html
<div dj-value="user.name|upper"></div>
```

```html
<div>{{ user.name|upper }}</div>
```

Void and self-closing tags are turned into paired tags so the value has a place to render:

```html
<img dj-value="avatar.url" />
```

```html
<img>{{ avatar.url }}</img>
```
