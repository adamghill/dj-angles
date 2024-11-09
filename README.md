<p align="center">
  <h1 align="center">dj-angles &lt;/&gt;</h1>
</p>

![PyPI](https://img.shields.io/pypi/v/dj-angles?color=blue&style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/dj-angles?color=blue&style=flat-square)
![GitHub Sponsors](https://img.shields.io/github/sponsors/adamghill?color=blue&style=flat-square)
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)

- 📖 Complete documentation: https://dj-angles.adamghill.com/
- 📦 Package: https://pypi.org/project/dj-angles/

## ⭐ Features

- Use HTML-like elements in Django templates, e.g. `<dj-partial />` instead of `{% include 'partial.html' %}`
- Wraps `include` templates in a custom element for easier debugging and targeted CSS styling
- Can be sprinkled in as needed to enhance existing Django functionality
- Since it looks like HTML, syntax highlighting mostly "just works"
- Integrates with Django component libraries like [django-bird](https://django-bird.readthedocs.io)
- Lets you excitedly tell your friends how neat the Shadow DOM is
- Pretend like you are writing React components, but without dealing with a JavaScript build process

## 💥 Example

**`base.html`**

```html
<dj-block name='content'>  <!-- {% block content %} -->
</dj-block>  <!-- {% endblock content %} -->
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
</dj-block>  <!-- {% endblock content %} -->
```

**partial.html**

```html
<div>
  This is a partial: {{ now|date:"c" }}
</div>
```

## 📖 Documentation

To learn how to install and use `dj-angles` see the complete documentation at https://dj-angles.adamghill.com/.

## ✨ Inspiration

- [Web Components](https://web.dev/learn/html/template)
- [Cotton](https://django-cotton.com) by [wrabit](https://github.com/wrabit)

## 🙌 Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="http://www.levit.be"><img src="https://avatars.githubusercontent.com/u/1215070?v=4?s=100" width="100px;" alt="Emmanuelle Delescolle"/><br /><sub><b>Emmanuelle Delescolle</b></sub></a><br /><a href="https://github.com/adamghill/dj-angles/commits?author=nanuxbe" title="Code">💻</a> <a href="https://github.com/adamghill/dj-angles/commits?author=nanuxbe" title="Tests">⚠️</a> <a href="https://github.com/adamghill/dj-angles/commits?author=nanuxbe" title="Documentation">📖</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
