# Settings

Settings can be configured via an `ANGLES` dictionary in `settings.py`.

## `slots_enabled`

Enables [slots](components.md#slots) functionality for components. `Boolean` which defaults to `False`.

## `initial_tag_regex`

The regex to know that particular HTML should be parsed by `dj-angles`. `Raw string` which defaults to `r"(dj-)"`.

## `lower_case_tag`

Lower-cases the tag. Deprecated and superseded by `kebab_case_tag`. `Boolean` which defaults to `False`.

## `kebab_case_tag`

Makes the tag kebab case based on upper case letter, e.g. "PartialOne" would get converted to "partial-one". `Boolean` which defaults to `True`.

## `mappers`

Provide additional mappers. `Dictionary` which defaults to `{}`. More details about [mappers](mappers.md).

## `default_mapper`

A default mapper. Useful for tighter integration with other component libraries. `String` which defaults to `"dj_angles.mappers.angles.default_mapper"`.

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
