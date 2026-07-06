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

## [`for`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#for)

```html
<li dj-for="i in items">{{ i }}</li>
```

```html
{% for i in items %}<li>{{ i }}</li>{% endfor %}
```

Self-closing tags are automatically paired so the loop has an element to render:

```html
<li dj-for="i in items" dj-value="i" />
```

```html
{% for i in items %}<li>{{ i }}</li>{% endfor %}
```

Nested loops work as expected:

```html
<tr dj-for="row in rows">
  <td dj-for="cell in row">{{ cell }}</td>
</tr>
```

```html
{% for row in rows %}<tr>{% for cell in row %}<td>{{ cell }}</td>{% endfor %}</tr>{% endfor %}
```

Django's `forloop` variables (`forloop.counter`, `forloop.first`, etc.) work without any special handling.

### `dj-empty`

Use a sibling element with `dj-empty` to render content when the loop has no items — equivalent to Django's [`{% empty %}`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#for-empty):

```html
<li dj-for="i in items">{{ i }}</li>
<li dj-empty>No items.</li>
```

```html
{% for i in items %}<li>{{ i }}</li>{% empty %}<li>No items.</li>{% endfor %}
```

### `dj-endfor`

An explicit `dj-endfor` on the closing tag can be used instead of relying on automatic `{% endfor %}` insertion:

```html
<li dj-for="i in items">{{ i }}</li dj-endfor>
```

```html
{% for i in items %}<li>{{ i }}</li>{% endfor %}
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
