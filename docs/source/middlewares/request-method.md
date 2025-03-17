# RequestMethodMiddleware

Adds the request's method as boolean properties to the `request` object.

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
        book.name = request.POST.get('name')
        book.save()

        return redirect('book', id=book.id)

    return render(request, 'book.html', {'book': book})
```

## Properties

- `request.is_post`
- `request.is_get`
- `request.is_patch`
- `request.is_head`
- `request.is_put`
- `request.is_delete`
- `request.is_trace`