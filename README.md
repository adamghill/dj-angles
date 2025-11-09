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
- Can be sprinkled in as needed to enhance existing Django functionality
- Since it looks like HTML, syntax highlighting mostly "just works"
- Wraps included templates in a custom element for easier debugging and targeted CSS styling
- Support for making components with the [Shadow DOM](https://dj-angles.adamghill.com/components/#CSS-scoping)
- Integrates with Django component libraries like [django-bird](https://django-bird.readthedocs.io) and [django-template-partials](https://github.com/carltongibson/django-template-partials)
- [`call`](template-tags/call.md) and [`model`](template-tags/model.md) template tags to call functions directly from a template
- [`dateformat`](filters/dateformat.md) filter to use Python [`strftime`](https://strftime.org) formats instead of PHP when formatting dates
- Submit forms via AJAX and swap in the resulting HTML

## 💥 Example

**base.html**

```html
<dj-block name='content'>  <!-- {% block content %} -->
</dj-block>  <!-- {% endblock content %} -->
```

**index.html**

```html
<dj-extends parent='base.html' />  <!-- {% extends 'base.html' %} -->

<dj-block name='content'>  <!-- {% block content %} -->
  <!-- components -->
  <dj-partial />  <!-- {% include 'partial.html' %} -->
  <dj-include template='partial.html' />  <!-- {% include 'partial.html' %} -->

  <!-- evaluate code from the template -->
  <dj-call code='slugify("Hello Goodbye")' as='variable_name' />  <!-- {% call slugify("Hello Goodbye") as variable_name %} -->
  <dj-model code='Book.objects.filter(id=1)' as='book' />  <!-- {% model Book.objects.filter(id=1) as book %} -->

  <!-- AJAX form submission -->
  <dj-form action='/submit' method='POST' swap='outerHTML' ajax csrf> <!-- <ajax-form><form action='/submit' method='POST'>{% csrf_token %} -->
    <button type='submit'>Submit</button>
  </dj-form><!-- </form></ajax-form> -->

  <!-- conditional attributes -->
  <div dj-if="True">  <!-- {% if True %}<div> -->
    If
  </div>
  <div dj-elif="False">  <!-- {% elif False %}<div> -->
    Elif
  </div>
  <div dj-else>  <!-- {% else %}<div> -->
    Else
  </div>  <!-- </div>{% endif %} -->

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

  <!-- static helpers -->
  <dj-image src='img/django.jpg' />  <!-- <img src="{% static 'img/django.jpg' %}" /> -->
  <dj-css href='css/styles.css' />  <!-- <link href="{% static 'css/styles.css' %}" rel="stylesheet" /> -->
</dj-block>  <!-- {% endblock content %} -->
```

## 📖 Documentation

To learn how to install and use `dj-angles` see the complete documentation at https://dj-angles.adamghill.com/.

## 🧩 Django Component Libraries

There are a growing number of component libraries for Django. A non-complete list:

- [Slippers](https://mitchel.me/slippers/): Build reusable components in Django without writing a single line of Python.
- [django-components](https://django-components.github.io/django-components/): Create simple reusable template components in Django.
- [django-template-partials](https://github.com/carltongibson/django-template-partials): Reusable named inline partials for the Django Template Language.
- [django-bird](https://django-bird.readthedocs.io): High-flying components for perfectionists with deadlines.
- [django-cotton](https://django-cotton.com): Enabling Modern UI Composition in Django.
- [django-viewcomponent](https://github.com/rails-inspire-django/django-viewcomponent): Build reusable components in Django, inspired by Rails ViewComponent.
- [django-unicorn](https://www.django-unicorn.com): The magical reactive component framework for Django ✨.

## ✨ Inspiration

- [Web Components](https://web.dev/learn/html/template)
- [django-cotton](https://django-cotton.com) by [wrabit](https://github.com/wrabit)

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
