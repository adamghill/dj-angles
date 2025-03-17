# Introduction

## ⭐ Features

- Use HTML-like elements in Django templates, e.g. `<dj-partial />` instead of `{% include 'partial.html' %}`
- Can be sprinkled in as needed to enhance existing Django functionality
- Since it looks like HTML, syntax highlighting mostly "just works"
- Wraps included templates in a custom element for easier debugging and targeted CSS styling
- Support for making components with the [Shadow DOM](components.md#css-scoping)
- Integrates with Django component libraries like [django-bird](https://django-bird.readthedocs.io)
- [`call`](template-tags/call.md) and [`model`](template-tags/model.md) template tags to call functions directly from a template
- [`dateformat`](filters/dateformat.md) filter to use Python [`strftime`](https://strftime.org) formats instead of PHP when formatting dates
- Submit forms via AJAX and swap in the resulting HTML

## 💥 Example

**base.html**

```
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

## ✨ Inspiration

- [Web Components](https://web.dev/learn/html/template)
- [Cotton](https://django-cotton.com) by [wrabit](https://github.com/wrabit)

```{toctree}
:maxdepth: 2
:hidden:

self
installation
components
tag-elements
tag-attributes
examples
```

```{toctree}
:caption: Filters
:maxdepth: 2
:hidden:

filters/dateformat
```

```{toctree}
:caption: Template Tags
:maxdepth: 2
:hidden:

template-tags/call
template-tags/model
```

```{toctree}
:caption: Custom Elements
:maxdepth: 2
:hidden:

custom-elements/ajax-form
```

```{toctree}
:caption: Middlewares
:maxdepth: 2
:hidden:

middlewares/request-method
middlewares/request-ajax
```

```{toctree}
:caption: Integrations
:maxdepth: 2
:hidden:

integrations/django-bird
```

```{toctree}
:caption: Advanced
:maxdepth: 2
:hidden:

settings
mappers
```

```{toctree}
:caption: API
:maxdepth: 3
:hidden:

api/dj_angles/index
```

```{toctree}
:caption: Info
:maxdepth: 2
:hidden:

changelog
GitHub <https://github.com/adamghill/dj-angles>
Sponsor <https://github.com/sponsors/adamghill>
```
