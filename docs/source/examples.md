# Examples

`dj-angles` is pretty flexible when determining what HTML to parse. Here are some examples to show what can be done. [Custom mappers](mappers.md) can also be setup to handle additional use cases.

## Tags without a dj- prefix

```python
# settings.py

ANGLES = {
  "initial_tag_regex": r"(?=\w)",  # lookahead match anything that starts with a letter
  "map_explicit_tags_only": True,  # only map tags we know about to prevent mapping standard HTML tags
}
```

```text
<block name='content'>
  <include 'partial.html' />
</block>
```

This would transpile to the following.

```text
{% block content %}
  <dj-partial>{% include 'partial.html' %}</dj-partial>
{% endblock content %}
```

## React-style include

```python
# settings.py

ANGLES = {
  "initial_tag_regex": r"(?=[A-Z])",  # lookahead match upper-case letter
}
```

```html
<PartialOne />
```

This would transpile to the following.

```text
<dj-partial>{% include 'partial-one.html' %}</dj-partial>
```

## Tags with a special character

```python
# settings.py

ANGLES = {
  "initial_tag_regex": r"(\$)"
}
```

```text
<$partial />
```

This would transpile to the following.

```text
<dj-partial>{% include 'partial.html' %}</dj-partial>
```

## Attributes without a dj- prefix

```python
# settings.py

ANGLES = {
  "initial_attribute_regex": r"(?=\w)",  # lookahead match anything that starts with a letter
}
```

```text
<div if="True">Example</div>
```

This would transpile to the following.

```text
{% if True %}<div if="True">Example</div>{% endif %}
```


## Attributes with a special character

```python
# settings.py

ANGLES = {
  "initial_attribute_regex": r"(:)",
}
```

```text
<div :if="True">Example</div>
```

This would transpile to the following.

```text
{% if True %}<div if="True">Example</div>{% endif %}
```
