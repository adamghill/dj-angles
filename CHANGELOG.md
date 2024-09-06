# Changelog

## 0.3.0-dev

- Wrap all includes in a custom element for easier debugging and targeted CSS styling.
- Support ":" to append additional identifier to the custom wrapping element.
- Fix: handle "shadow" being in the template name.

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
