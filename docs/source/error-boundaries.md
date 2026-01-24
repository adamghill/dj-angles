# Error Boundaries

Error boundaries are a way to handle errors in included templates. Instead of the yellow screen of death that shows an entire traceback, the error will be contained to the error boundary.

## Block

An `error-boundary` attribute can be added to a `dj-block` to enable error boundaries. If any error occurs within that block, an error message will be displayed.

```html
<dj-block name='content' error-boundary>
  <dj-include src="missing-template.html" />
</dj-block>
```

## Element

A `dj-error-boundary` element can be used to wrap any HTML. If any error occurs within the element, an error message will be displayed.

```html
<dj-error-boundary>
  <dj-include src="missing-template.html" />
</dj-error-boundary>
```

### `default`

A default template to render if an error occurs. This can be a string or a template path.

```html
<dj-error-boundary default="There was an error!">
    <dj-include src="missing-template.html" />
</dj-error-boundary>
```

```html
<dj-error-boundary default="error-template.html">
    <dj-include src="missing-template.html" />
</dj-error-boundary>
```
