# Changelog

## 0.22.0-dev

- Add integration with [`django-template-partials`](https://github.com/carltongibson/django-template-partials).

## 0.21.0

- Add `no-wrap` attribute to [components](components.md).
- Add `class` attribute to [components](components.md).

## 0.20.0

- Fix `django-bird` integration when using the default mapper. [#16](https://github.com/adamghill/dj-angles/pull/16) from [benbacardi](https://github.com/benbacardi).

## 0.19.0

- Fix `delay` in `ajax-form`.
- Add `template` template tag.
- Return a stringified result from `call` template tag.

### Breaking changes

- Remove automatically casting strings to `UUID`, `datetime`, `date`, or `time`. That can be done manually in the function if needed and it's a little too magical.

## 0.18.0

- Add `ajax-form` custom element.
- Add `form` tag element.
- Add `RequestMethodMiddleware` and `RequestAJAXMiddleware`.

## 0.17.0

- Add `dateformat` filter.

## 0.16.0

- Add `dj-call` and `dj-model` tags.

## 0.15.0

- Add `call` and `model` template tags.

## 0.14.1

- Support conditional attributes on `dj` tags, e.g. `dj-include`.

## 0.14.0

- Add support for `dj-if`, `dj-elif`, `dj-else` attributes.
- Add `initial_attribute_regex` setting.

## 0.13.1

- Better handling of spaces and tabs in template tag arguments.

## 0.13.0

- Handle newlines in template tag arguments.

## 0.12.0

- Self-closing `dj-block` tag; `<dj-block name='content' />` would translate to `{% block content %}{% endblock content %}`.
- Handle template includes that begin with an underscore; `<dj-partial />` would translate to, in order, either `partial.html` or `_partial.html` depending on which template file was found.

## 0.11.0

- Use the start tag's `name` for `dj-block` end tag if possible.

## 0.10.0

- Add `default_mapper` based on [#7](https://github.com/adamghill/dj-angles/pull/7) from [nanuxbe](https://github.com/nanuxbe).

## 0.9.0

- Add (beta) named slots implementation. Enable with `ANGLES={"enable_slots": True}` in settings.
- Fix: End wrapping tag was sometimes incorrect for some includes.

## 0.8.1

- Create tag mappers once and cache it.

## 0.8.0

- Add integration with [`django-bird`](https://django-bird.readthedocs.io/).

**Breaking changes**

- Dropped support for Python 3.8.

## 0.7.0

- Add support for the following attributes and tags for better HTML lintability:
    - `template` attribute for `include`
    - `name` attribute for `block`
    - `parent` attribute for `extends`
    - `href` attribute for `css`
    - `src` attribute for `image`

## 0.6.1

- Remove `uv.lock` from build.

## 0.6.0

- Raise more explicit exceptions in some edge cases.
- Re-write all documentation and add missing docstrings.

## 0.5.0

- Add `dj-image` and `dj-css` which automatically uses the static template tag.

## 0.4.0

- Raise `InvalidEndTag` if a tag is not closed properly.
- Fix: lots of edge-cases.

**Breaking changes**

- Pass `Tag` object to mapper functions instead of arguments to better encapsulate functionality.

## 0.3.0

- Wrap all includes in a custom element for easier debugging and targeted CSS styling.
- Support ":" to append additional identifier to the custom wrapping element.
- Fix: support "shadow" being in the template name.

## 0.2.0

- Add `initial_tag_regex` setting.
- Add `lower_case_tag` setting.
- Add `mappers` setting.

**Breaking changes**

- Removed default support for starting tags with a `$`, however the same functionality can be configured in settings.

## 0.1.1

- Fix `csrf-input`.

## 0.1.0

- Initial release.
