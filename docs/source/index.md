# Introduction

## ⭐ Features

- Use HTML-like elements in Django templates, e.g. `<dj-partial />` instead of `{% include 'partial.html' %}`
- Can be sprinkled in as needed to enhance existing Django functionality
- Since it looks like HTML, syntax highlighting mostly "just works"
- Wraps included templates in a custom element for easier debugging and targeted CSS styling
- Support for making components with the [Shadow DOM](components.md#css-scoping)
- Integrates with Django component libraries like [django-bird](https://django-bird.readthedocs.io)

## 💥 Example

**base.html**

```
<dj-block name='content'>  <!-- {% block content %} -->
</dj-block>  <!-- {% endblock content %} -->
```

**index.html**

```
<dj-extends parent='base.html' />  <!-- {% extends 'base.html' %} -->

<dj-block name='content'>  <!-- {% block content %} -->
  <dj-partial />  <!-- {% include 'partial.html' %} -->

  <div dj-if="True">  <!-- {% if True %}<div> -->
    If
  </div>
  <div dj-elif="False">  <!-- {% elif False %}<div> -->
    Elif
  </div>
  <div dj-else>  <!-- {% else %}<div> -->
    Else
  </div>  <!-- </div>{% endif %} -->

  <dj-include template='partial.html' />  <!-- {% include 'partial.html' %} -->

  <dj-verbatim>  <!-- {% verbatim %} -->
    This is verbatim: {% include %}
  </dj-verbatim>  <!-- {% endverbatim %} -->

  <dj-comment>  <!-- {% comment %} -->
    this is a comment
  </dj-comment>  <!-- {% endcomment %} -->

  <dj-#>this is another comment</dj-#>    <!-- {# this is another comment #} -->

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
