# Call

The `call` template tag allows functions to be called from within a template.

```{note}
Make sure to include `{% load dj_angles %}` in your template or add `dj_angles.templatetags.dj_angles` to `TEMPLATES["OPTIONS"]["builtins"]`.
```

## Example

Lets say you have a `Book` model and you want to list all of the books, but add an icon if the book has been read by the current user.

### Models

```python
# models.py
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=100)

    def is_read(self, request):
        if request.user.is_anonymous:
            return False

        return self.readers.filter(user=request.user).exists()

class Reader(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', related_name='readers', on_delete=models.CASCADE)
```

### Template

There are a few different ways to show an icon if a book has been read.

```{note}
All of these examples result in n+1 queries, but the code is kept simple just as an example.
```

#### Add an attribute to the model in the view

This feels a little clunky and adds an implicit attribute to the model which is not very discoverable.

```python
# views.py
from django.shortcuts import render
from book.models import Book

def index(request):
    books = Book.objects.all()

    # Loop over all books and add an attribute
    for book in books:
        book.current_user_read = book.is_read(request)

    return render(request, 'index.html', {'books': books})
```

```html
<!-- index.html -->
{% for book in books %}
<div>
  {{ book.title }}

  {% if book.current_user_read %}
  ✅
  {% else %}
  ❌
  {% endif %}
</div>
{% endfor %}
```

#### Make a custom template tag

This encapsulates template logic in Python code so it can be tested. However, it requires extra code for every use case and can feel like additional work especially for "pass-through" template tags which just call a function.

```python
# views.py
from django.shortcuts import render
from book.models import Book

def index(request):
    books = Book.objects.all()

    return render(request, 'index.html', {'books': books})
```

```python
# templatetags/book_tags.py
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def current_user_read(context, book):
    return book.is_read(context['request'])
```

```html
<!-- index.html -->
{% load book_tags %}

{% for book in books %}
<div>
  {{ book.title }}

  {% if current_user_read book %}
  ✅
  {% else %}
  ❌
  {% endif %}
</div>
{% endfor %}
```

#### Use the `call` template tag

This is basically like a "pass-through" template tag, but without the extra hassle of creating a custom template tag every time.

```python
# views.py
from django.shortcuts import render
from book.models import Book

def index(request):
    books = Book.objects.all()

    return render(request, 'index.html', {'books': books})
```

```html
<!-- index.html -->
{% for book in books %}
<div>
  {{ book.title }}

  {% call book.is_read(request) as current_user_read %}

  {% if current_user_read %}
  ✅
  {% else %}
  ❌
  {% endif %}
</div>
{% endfor %}
```

## Calling functions

The template tag function argument tries to look as similar to normal Python code as possible. It is followed by the word "as" and then a variable name that will store the result of the function in the context for use later.

```html
{% call slugify('Hello Goodbye') as slug %}

{{ slug }} <!-- hello-goodbye -->
```

The `call` template tag can only call functions that are available in the context. So, the `slugify` function needs to be added to the context in the view.

```python
# views.py
from django.shortcuts import render
from django.utils.text import slugify

def index(request):
    return render(request, 'index.html', {'slugify': slugify})
```

## Traversing

### Objects

```html
{% call django.utils.text.slugify('Hello Goodbye') as slug %}

{{ slug }} <!-- hello-goodbye -->
```

```python
# views.py
from django.shortcuts import render
import django

def index(request):
    return render(request, 'index.html', {'django': django})
```

### Dictionaries

```python
# views.py
from django.shortcuts import render
import django

def index(request):
    data = {"functions": {"slugify": django.utils.text.slugify}}
    return render(request, "index.html", {"data": data})
```

```html
{% call data.functions.slugify('Hello Goodbye') as slug %}

{{ slug }} <!-- hello-goodbye -->
```

## Supported argument types

Most Python primitives are supported as arguments, e.g. strings, ints, lists, dictionaries, etc. There is also special handling for strings that appear to be datetimes, dates, times, durations, or UUIDs.

```html
{% call add(2, 3) as result %}

{{ result }} <!-- 5 -->
```

```python
# views.py
from django.shortcuts import render

def index(request):
    return render(request, 'index.html', {'add': lambda a, b: a + b})
```

### Datetimes

```html
{% call add_day("2025-03-14") as next_day %}

{{ next_day }} <!-- 2025-03-15 -->
```

```python
# views.py
from django.shortcuts import render
from datetime import timedelta

def index(request):
    return render(request, 'index.html', {'add_day': lambda dt: dt + timedelta(days=1)})
```

## Template variables

Django template variables can be used for args or kwargs as long as they are available in the context.

```html
{% call add(number_one, number_two) as result %}

{{ result }} <!-- 3 -->
```

```python
# views.py
from django.shortcuts import render

def index(request):
    return render(request, 'index.html', {'add': lambda a, b: a + b, 'number_one': 1, 'number_two': 2})
```

```{note}
If a variable is referred to, but is not available a VariableNotFound error will be raised.
```

## Unpacking

Args and kwargs can be unpacked using the `*` and `**` operators.

### Args

```html
<!-- index.html -->
{% call add(*[2, 3]) as result %}

<!-- equivalent using template variable -->
{% call add(*numbers) as result %}

<!-- equivalent without unpacking -->
{% call add(2, 3) as result %}

{{ result }} <!-- 5 -->
```

```python
# views.py
from django.shortcuts import render

def index(request):
    return render(request, 'index.html', {'add': lambda a, b: a + b, 'numbers': [2, 3]})
```

### Kwargs

```html
<!-- index.html -->
{% call make_name(**{'first_name': 'Alice', 'last_name': 'Smith'}) as result %}

<!-- equivalent using template variable -->
{% call make_name(**name) as result %}

<!-- equivalent without unpacking -->
{% call make_name(first_name='Alice', last_name='Smith') as result %}

{{ result }} <!-- Alice Smith -->
```

```python
# views.py
from django.shortcuts import render

def make_name(first_name, last_name):
    return f"{first_name} {last_name}"

def index(request):
    return render(request, 'index.html', {'make_name': make_name, 'name': {'first_name': 'Alice', 'last_name': 'Smith'}})
```

## Querysets

```html
<!-- index.html -->
{% call books.filter(published__gte='2020-01-01').order_by('name') as books %}

<ul>
{% for book in books %}
<li>{{ book }}</li>
{% endfor %}
</ul>
```

```python
# views.py
from django.shortcuts import render
from book.models import Book

def index(request):
    books = Book.objects.all()
    return render(request, 'index.html', {'books': books})
```
