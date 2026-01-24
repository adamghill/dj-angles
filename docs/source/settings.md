# Settings

Settings can be configured via an `ANGLES` dictionary in `settings.py`.

```python
# settings.py

ANGLES = {}
```

## `default_mapper`

A default mapper. Useful for tighter integration with other component libraries. `String` which is an import path. Defaults to `"dj_angles.mappers.angles.default_mapper"`.

```python
# settings.py

ANGLES = {
  "default_mapper": "dj_angles.mappers.angles.default_mapper"
}
```

### `"dj_angles.mappers.angles.default_mapper"` (the default)

```html
<dj-blob />
```

Would be transpiled to the following.

```html
<dj-blob>{% include 'blob.html' %}</dj-blob>
```

### `"dj_angles.mappers.thirdparty.map_bird"`

```html
<dj-blob />
```

Would be transpiled to the following.

```html
<dj-blob>{% bird blob / %}</dj-blob>
```

## `initial_attribute_regex`

The regex for `dj-angles` attributes, e.g. `dj-if`. `Raw string` which defaults to `r"(dj-)"`.

## `initial_tag_regex`

The regex to know that particular HTML should be parsed by `dj-angles`. `Raw string` which defaults to `r"(dj-)"`.

## `kebab_case_tag`

Makes the tag kebab case based on upper case letter, e.g. "PartialOne" would get converted to "partial-one". `Boolean` which defaults to `True`.

## `lower_case_tag`

Lower-cases the tag. Deprecated and superseded by `kebab_case_tag`. `Boolean` which defaults to `False`.

## `map_explicit_tags_only`

Do not fallback to the default if a mapper cannot be found. `Boolean` which defaults to `False`.

## `mappers`

Custom additional mappers. `Dictionary` which defaults to `{}`. More details about [mappers](mappers.md).

## `slots_enabled`

Enables [slots](components.md#slots) functionality for components. `Boolean` which defaults to `False`.

## `error_boundaries`

Settings for [error boundaries](error-boundaries.md) functionality. `dict` which defaults to `{}`.

### `enabled`

Enables error boundaries. `Boolean` which defaults to `True`.

### `shadow`

Encapsulates error boundary errors with Shadow DOM. `Boolean` which defaults to `True`.

### `class`

The class to apply to error boundaries. `String` which defaults to `""`.

### `style`

The style to apply to error boundaries. `String` which defaults to `"border: 1px red solid; padding: 0 24px 0 24px;"`.

```python
# settings.py
ANGLES = {
  "error_boundaries": {"enabled": True, "shadow": True, "class": "", "style": "border: 1px red solid; padding: 0 24px 0 24px;"}
}
```
