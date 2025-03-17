# ajax-form

The `ajax-form` is a custom element which wraps around a regular HTML `form` element, but submits the form data via AJAX. This allows the form to be submitted without a page reload, similar to using [HTMX](https://htmx.org/) and the `hx-swap` functionality.

```{note}
Make sure to [install `dj_angles` middleware](../installation.md#middleware) to use `is_post` and `is_ajax`. The `dj_angles` scripts also must be [included in the HTML template](../installation.md#scripts).
```

## Example

```python
# views.py
from django.shortcuts import render
from book.models import Book

def book(request, book_id):        
    book = Book.objects.filter(id=book_id).first()

    if request.is_post:
        book.title = request.POST.get('title')
        book.save()

        if not request.is_ajax:
            return redirect('book', id=book.id)

    return render(request, 'book.html', {'book': book})
```

```html
<ajax-form>
  <form action='/submit' method='POST'>
    {% csrf_token %}

    <input type="text" value="{{ book.title }}">
    <button type="submit">Submit</button>
  </form>
</ajax-form>
```

### `form` tag

The custom element can be used directly, but there is a shortcut [`form` tag element](../tag-elements.md#form) as well.

```html
<dj-form action='/submit' method='POST' ajax csrf>
  <input type="text" value="{{ book.title }}">
  <button type="submit">Submit</button>
</dj-form>
```

## Attributes

### `swap`

Defines how the form should be replaced after submission. Valid values are `outerHTML` and `innerHTML`. Defaults to `outerHTML`.

```html
<ajax-form swap='outerHTML'>
  <form action='/submit' method='POST'>
    {% csrf_token %}

    <input type="text" value="{{ book.title }}">
    <button type="submit">Submit</button>
  </form>
</ajax-form>
```

### `delay`

Defines the delay in milliseconds before the form is submitted. Defaults to 0.

```html
<ajax-form delay='1000'>
  <form action='/submit' method='POST'>
    {% csrf_token %}

    <input type="text" value="{{ book.title }}">
    <button type="submit">Submit</button>
  </form>
</ajax-form>
```
