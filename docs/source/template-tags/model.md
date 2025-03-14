# Model

The `model` template tag is a specialized version of the `call` template tag that automatically makes all database models available to be queried from the template without passing the model class into the context.

```html
{% model Book.objects.filter(published__gte='2020-01-01') as books %}

<br />
{% for book in books %}
<div>{{ book }}</div>
{% endfor %}
```

```python
# views.py
from django.shortcuts import render

def index(request):
    return render(request, 'index.html', {})
```
