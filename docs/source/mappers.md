# Mappers

`dj-angle` is built on the basic flow of:
1. parse template HTML with regex
2. look up a mapper for any matches found
3. handle string or callables mapper values appropriately

`dj-angles` includes a dictionary of built-in mappers. However, custom mappers can be added to handle other use cases.

## Custom mappers

The key of the dictionary is a string and is the text match of the regex after the `initial_tag_regex`, i.e. for the default `initial_tag_regex` of `r"(dj-)"`, the key would be the result after "dj-" until a space or a ">". For example, if "<dj-include 'partial.html' />" was in the HTML, "include" would be looked up in the mapper dictionary to determine what to do with that tag. 

The value can either be a string or a callable.

### string value

When the dictionary value is a string, it replaces the `initial_tag_regex` plus the key, and puts it between "{%" and the arguments plus "%}".

```python
# settings.py

ANGLES = {
    "mappers": {
        "component": "include",
    },
}
```

```text
<dj-component 'partial.html' />
```

Would compile to the following Django template.

```text
{% include 'partial.html' %}
```

### Callable value

When the dictionary value is a callable, the string result is dictated by the output of the mapper function. The callable has one argument, `Tag`, which encapsulates information about the matched tag that can be useful in building custom functionality, e.g. `component_name`, `is_end`, `is_self_closing`, etc.

```python
# settings.py

from dj_angles import Tag

def map_text(tag: Tag) -> str:
    return "This is some text."

def map_hello(tag: Tag) -> str:
    return f"<p>{tag.component_name.upper()}! {tag.template_tag_args}</p>"

ANGLES = {
    "mappers": {
        "text": map_text,
        "hello": map_hello,
    },
}
```

```text
<dj-text />

<dj-hello 'Goodbye!' />
```

Would compile to the following Django template.

```html
This is some text.

<p>HELLO! Goodbye!</p>
```
