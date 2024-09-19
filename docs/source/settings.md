# Settings

Settings can be configured via an `ANGLES` dictionary in `settings.py`.

```python
ANGLES = {}
```

## `initial_tag_regex`

Determines the characters that are used to indicate a `dj-angles` element. `String` which defaults to `r"(dj-)"`.

### Special character

```python
# settings.py

ANGLES = {
  "initial_tag_regex": r"(dj-|\$)"
}
```

```text
<dj-include 'partial.html' />
<dj-partial />
<$partial />
```

These would all compile to the following Django template.

```text
{% include 'partial.html' %}
```

### React-style include

```python
# settings.py

ANGLES = {
  "initial_tag_regex": r"(dj-|(?=[A-Z]))",  # regex matches "dj-" or upper-case letter lookahead
  "lower_case_tag": True,  # without this the template `Partial.html` will be loaded
}
```

```text
<dj-include 'partial.html' />
<dj-partial />
<Partial />
```

These would all compile to the following Django template.

```text
{% include 'partial.html' %}
```

## `lower_case_tag`

Lower-cases the tag. Useful when using [React-style includes](#react-style-include) to convert something like "Partial" to "partial" for the name of the template. `Boolean` which defaults to `False`.

## `mappers`

Provide additional mappers. `Dictionary` which defaults to `{}`. More details about [mappers](mappers.md).