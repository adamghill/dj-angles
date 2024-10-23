# Settings

Settings can be configured via an `ANGLES` dictionary in `settings.py`.

## `slots_enabled`

Enables [slots](components.md#slots) functionality for components. `Boolean` which defaults to `False`.

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
<dj-partial>{% include 'partial.html' %}</dj-partial>
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

## `default_mapper`

A default mapper. Useful for tighter integration with other component libraries. `String` which defaults to `"dj_angles.mappers.angles.default_mapper"` which is basically the same as the normal mapper for the `include` template tag.

Example settings:

```python
# settings.py

ANGLES = {
  "default_mapper": "dj_angles.mappers.angles.default_mapper"
}
```

### `"dj_angles.mappers.angles.default_mapper"` (the default)

```html
<dj-partial />
```

Would be translated to the following.

```html
<dj-partial>{% include 'partial.html' %}</dj-partial>
```

### `"dj_angles.mappers.thirdparty.map_bird"`

```html
<dj-partial />
```

Would be translated to the following.

```html
<dj-partial>{% bird partial / %}</dj-partial>
```
