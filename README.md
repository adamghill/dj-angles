<p align="center">
  <h1 align="center">dj-angles &lt;/&gt;</h1>
</p>
<p align="center">Add more bracket angles to Django templates</p>

![PyPI](https://img.shields.io/pypi/v/dj-angles?color=blue&style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/dj-angles?color=blue&style=flat-square)
![GitHub Sponsors](https://img.shields.io/github/sponsors/adamghill?color=blue&style=flat-square)
[![All Contributors](https://img.shields.io/github/all-contributors/adamghill/dj-angles?color=ee8449&style=flat-square)](#contributors)

- 📖 Full documentation: https://dj-angles.adamghill.com/
- 📦 Package is on PyPI: https://pypi.org/project/dj-angles/

## ⭐ Features

- Use HTML-like elements in Django templates, e.g. `<dj-partial />` instead of `{% include 'partial.html' %}`
- Wraps `include` templates in a custom element for easier debugging and targeted CSS styling
- Can be sprinkled in as needed to enhance existing Django functionality
- Since it looks like HTML, syntax highlighting mostly "just works"
- Integrates with Django component libraries like [django-bird](https://django-bird.readthedocs.io)
- Lets you excitedly tell your friends how neat the Shadow DOM is
- Pretend like you are writing React components, but without dealing with JavaScript at all

## 💥 Example

**`base.html`**

```html
<dj-block name='content'>
</dj-block name='content'>
```

**`index.html`**

```html
<dj-extends parent='base.html' />  <!-- {% extends 'base.html' %} -->

<dj-block name='content'>  <!-- {% block content %} -->
  <dj-include template='partial.html' />  <!-- {% include 'partial.html' %} -->

  <dj-verbatim>  <!-- {% verbatim %} -->
    This is verbatim: {% include %}
  </dj-verbatim>  <!-- {% endverbatim %} -->

  <dj-comment>  <!-- {% comment %} -->
    this is a comment
  </dj-comment>  <!-- {% endcomment %} -->

  <dj-autoescape-on>  <!-- {% autoescape-on %} -->
    This is escaped
  </dj-autoescape-on>  <!-- {% endautoescape %} -->

  <dj-autoescape-off>  <!-- {% autoescape off %} -->
    This is not escaped
  </dj-autoescape-off>  <!-- {% endautoescape %} -->

  <dj-csrf />  <!-- {% csrf_token %} -->
  
  <dj-debug />  <!-- {% debug %} -->

  <dj-image src='img/django.jpg' />  <!-- <img src="{% static 'img/django.jpg' %}" /> -->
  <dj-css href='css/styles.css' />  <!-- <link href="{% static 'css/styles.css' %}" rel="stylesheet" /> -->
</dj-block name='content'>  <!-- {% endblock content %} -->
```

**partial.html**

```html
<div>
  This is a partial: {{ now|date:"c" }}
</div>
```

## 📖 Documentation

To learn more about how to install and use `dj-angles` go to https://dj-angles.adamghill.com/.

## ✨ Inspiration

I have been interested in Django components and encapsulating functionality for a long time (see [django-unicorn](https://www.django-unicorn.com), [dlitejs](https://dlitejs.com), etc), but had never thought of using HTML directly until I looked at [Cotton](https://django-cotton.com) by [wrabit](https://github.com/wrabit). `dj-angles` takes the initial idea further to see how well it works.

## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
