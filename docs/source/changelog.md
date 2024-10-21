# Changelog

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
