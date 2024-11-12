# Components

`dj-angles` provides component-like functionality by enhancing Django's built-in `include` template tag.

## Includes

These are equivalent ways to include HTML files.

```text
<dj-partial />
<dj-include template='partial.html' />
<dj-include template='partial' />
<dj-include 'partial.html' />
<dj-include 'partial' />
```

```{note}
The self-closing element is used in most examples, but explicit closing elements for all examples, e.g. `<dj-partial></dj-partial>`, also works.
```

They all compile to the following Django template.

```html
<dj-partial>{% include 'partial.html' %}</dj-partial>
```

The wrapping element, e.g. `dj-partial`, is a custom element which browsers will ignore. It allows for easier debugging when looking at the source code and also allows for targeted CSS styling.

```{warning}
The built-in [tags](tag-elements.md) are considered reserved words. Template file names that conflict will not get loaded because reserved words take precedence. For example, if there is a template named "extends.html" `<dj-extends />` could not be used to include it; `<dj-include 'extends.html' />` would need to be used instead.
```

### Underscored files

Underscores are used as a convention for partials in some frameworks, so that is supported in `dj-angles`. The following would first look for `partial.html`. If it could not be found, it would then look for `_partial.html`.

```html
<dj-partial />
```

### Wrapping element key

Adding a colon and an identifier to the end of a template name allows for even more specific CSS styling.

```html
<dj-partial:1 />
```

Would get compiled to the following Django template.

```html
<dj-partial-1>{% include 'partial.html' }</dj-partial-1>
```

### Directories

Accessing templates in directories is supported even though technically forward-slashes [aren't permitted in a custom element](https://html.spec.whatwg.org/multipage/custom-elements.html#valid-custom-element-name). It might confound HTML syntax highlighters.

```text
<dj-directory/partial />
<dj-include template='directory/partial.html' />
<dj-include template='directory/partial' />
<dj-include 'directory/partial.html' />
<dj-include 'directory/partial' />

```

They all compile to the following Django template.

```html
<dj-directory-partial>{% include 'directory/partial.html' %}</dj-directory-partial>
```

## CSS scoping

To encapsulate component styles, the `dj-angles` can use the Shadow DOM. This will ensure that any `style` element in the include will be contained. The downside is that the Shadow DOM does not allow outside styles in (other than CSS variables).

These are all equivalent ways to use the Shadow DOM with an include.

```text
<dj-partial! />
<dj-partial shadow />
<dj-include template='partial.html' shadow />
<dj-include template='partial' shadow />
<dj-include 'partial.html' shadow />
<dj-include 'partial' shadow />
```

They all compile to the following Django template syntax.

```html
<dj-partial><template shadowrootmode='open'>{% include 'partial.html' %}</template></dj-partial>
```

**More information about the Shadow DOM**

- Shadow DOM styling: https://javascript.info/shadow-dom-style
- Declaratively creating a shadow root: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/template#shadowrootmode
- Using the Shadow DOM: https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_shadow_DOM

## Slots

```{note}
Currently in beta and disabled by default. Can be enabled by [setting `slots_enabled` to `True`](settings.md#slots_enabled).
```

Slots designate certain sections of an include template as placeholders. Those placeholders can then be "filled-in" with HTML when the component is rendered.

```html
<!-- index.html -->
<dj-include template="profile.html">
    <span slot="username">User One</span>
</dj-include>

<dj-include template="profile.html"></dj-include>
```

```html
<!-- profile.html -->
<h1>Profile</h1>

<ul>
    <li>Username: <slot name="username">n/a</slot></li>
</ul>
```

Would be rendered as the following.

```html
<dj-profile>
    <h1>Profile</h1>

    <ul>
        <li>Username: <slot name="username"><span slot="username">User One</span></slot></li>
    </ul>
</dj-profile>

<dj-profile>
    <h1>Profile</h1>

    <ul>
        <li>Username: <slot name="username">n/a</slot></li>
    </ul>
</dj-profile>
```

## Integrations

For other approaches to components in Django, `dj-angles` integrates with other Django component libraries. The currently supported external libraries include:

- [`django-bird`](integrations/django-bird.md)
