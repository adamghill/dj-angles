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

- Use HTML-like elements in Django templates, e.g. `<dj-some-partial />` instead of `{% include 'some-partial.html' %}`
- Can be sprinkled in as needed to enhance existing Django functionality
- Since it looks like HTML, syntax highlighting mostly "just works"
- Wraps components in a custom HTML element for easier debugging and targeted CSS styling
- Support for the [Shadow DOM](https://dj-angles.adamghill.com/en/latest/components/#css-scoping) to encapsulate component styles
- Lightweight way to submit forms via AJAX and swap in the resulting HTML

### Component library integrations

- Support for Django 6.0 [template partials](https://docs.djangoproject.com/en/stable/ref/templates/language/#template-partials)
- [django-components](https://django-components.github.io/django-components/)
- [django-bird](https://django-bird.readthedocs.io)
- [django-template-partials](https://github.com/carltongibson/django-template-partials) for Django <6.0

### Template tags

- [`call`](https://dj-angles.adamghill.com/en/latest/template-tags/call/) and [`model`](https://dj-angles.adamghill.com/en/latest/template-tags/model/) to call functions directly from a template instead of creating custom template tags

### Filters

- [`dateformat`](https://dj-angles.adamghill.com/en/latest/filters/dateformat/) filter to use Python [`strftime`](https://strftime.org) formats instead of PHP for formatting dates

## 💥 Examples

```html
<!-- base.html -->
<dj-block name='content'>  <!-- {% block content %} -->
</dj-block>  <!-- {% endblock content %} -->
```

```html
<!-- template-tags.html -->
<dj-extends parent='base.html' />  <!-- {% extends 'base.html' %} -->

<dj-block name='content'>  <!-- {% block content %} -->
  <!-- components -->
  <dj-some-partial />  <!-- {% include 'test-partial.html' %} -->
  <dj-include template='test-partial.html' />  <!-- {% include 'test-partial.html' %} -->

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
</dj-block>  <!-- {% endblock content %} -->
```

```html
<!-- static-helpers.html -->
<dj-image src='img/django.jpg' />  <!-- <img src="{% static 'img/django.jpg' %}" /> -->
<dj-css href='css/styles.css' />  <!-- <link href="{% static 'css/styles.css' %}" rel="stylesheet" /> -->
```

```html
<!-- call-code-from-template.html -->
<dj-call code='slugify("Hello Goodbye")' as='variable_name' />  <!-- {% call slugify("Hello Goodbye") as variable_name %} -->
<dj-model code='Book.objects.filter(id=1)' as='book' />  <!-- {% model Book.objects.filter(id=1) as book %} -->
```

```html
<!-- inline-expressions.html -->
{{ request.user.username or request.user.email }}  <!-- {% if request.user.username %}{{ request.user.username }}{% else %}{{ request.user.email }}{% endif %} -->
{{ request.user.username if request.user.is_authenticated else 'Unknown' }}  <!-- {% if request.user.is_authenticated %}{{ request.user.username }}{% else %}Unknown{% endif %} -->
```

```html
<!-- ajax-form-submission.html -->
<dj-form action='/submit' method='POST' swap='outerHTML' ajax csrf> <!-- <ajax-form><form action='/submit' method='POST'>{% csrf_token %} -->
  <button type='submit'>Submit</button>
</dj-form><!-- </form></ajax-form> -->
```

```html
<!-- conditional-attributes.html -->
<div dj-if="True">  <!-- {% if True %}<div> -->
  If
</div>
<div dj-elif="False">  <!-- {% elif False %}<div> -->
  Elif
</div>
<div dj-else>  <!-- {% else %}<div> -->
  Else
</div>  <!-- </div>{% endif %} -->
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
      <td align="center" valign="top" width="14.28%"><a href="https://jasalt.dev"><img src="https://avatars.githubusercontent.com/u/2306521?v=4?s=100" width="100px;" alt="Jarkko Saltiola"/><br /><sub><b>Jarkko Saltiola</b></sub></a><br /><a href="https://github.com/adamghill/dj-angles/commits?author=jasalt" title="Documentation">📖</a></td>
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
