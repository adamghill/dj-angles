# Components

`dj-angles` provides component-like functionality by using Django's built-in `include` template tag. And, of course, it provides some syntactic sugar on top to make the developer experience a little bit better.

These are equivalent ways to include partial HTML files.

```text
<dj-include 'partial.html' />
<dj-include 'partial' />
<dj-partial />
```

They all compile to the following Django template.

```html
<dj-partial>{% include 'partial.html' %}</dj-partial>
```

The wrapping element (in this example: `<dj-partial>`) allows for easier debugging when looking at the source code and also allows for targeted CSS styling.

Note: The built-in [tags](tag-elements.md) are considered reserved words. Template file names that conflict will not get loaded because reserved words take precedence. For example, if there is a template named "extends.html" `<dj-extends />` could not be used to include it; `<dj-include 'extends.html' />` would need to be used instead.

## Appending an identifier to the wrapping element

Adding a colon and an identifier to the end of a template name allows for even more specific CSS styling.

```html
<dj-partial:1 />
```

Would get compiled to the following Django template.

```html
<dj-partial-1>{% include 'partial.html' }</dj-partial-1>
```

## ⤵️ Directories

Accessing templates in directories is supported even though technically forward-slashes [aren't permitted in a custom element](https://html.spec.whatwg.org/multipage/custom-elements.html#valid-custom-element-name). It might confound HTML syntax highlighters.

```text
<dj-include 'directory/partial.html' />
<dj-include 'directory/partial' />
<dj-directory/partial />
```

They all compile to the following Django template.

```html
<dj-directory-partial>{% include 'directory/partial.html' %}</dj-directory-partial>
```

## 🥷 CSS scoping

To encapsulate component styles, enable the Shadow DOM for the partial. This will ensure that any `style` element in the partial will be contained to that partial. The downside is that the Shadow DOM does not allow outside styles in (other than CSS variables).

These are all equivalent ways to include a shadow partial.

```text
<dj-include 'partial.html' shadow />
<dj-partial shadow />
<dj-partial! />
```

They all compile to the following Django template syntax.

```html
<dj-partial><template shadowrootmode='open'>{% include 'partial.html' %}</template></dj-partial>
```

**More information about the Shadow DOM**

- Shadow DOM styling: https://javascript.info/shadow-dom-style
- Declaratively creating a shadow root: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/template#shadowrootmode
- Using the Shadow DOM: https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_shadow_DOM

