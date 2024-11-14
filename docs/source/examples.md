# Examples

## Bare HTML

## React-style include

```python
# settings.py

ANGLES = {
  "initial_tag_regex": r"(?=[A-Z])",  # regex matches upper-case letter lookahead
  "slugify_tag": True,  # without this the template `PartialOne.html` will be loaded
}
```

```text
<PartialOne />
```

This would transpile to the following.

```text
<dj-partial>{% include 'partial-one.html' %}</dj-partial>
```

## Special character

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

