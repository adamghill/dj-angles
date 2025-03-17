# RequestAJAXMiddleware

Adds whether the request is AJAX as a boolean property to the `request` object. Useful to check when rendering a view's HTML via AJAX, i.e. using the [`form` tag](../tag-elements.md#form) or [HTMX](https://htmx.org/).

```{note}
Make sure to [install `dj_angles` middleware](../installation.md#middleware) to access this functionality.
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

## Properties

- `request.is_ajax`
