# Changelog

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
