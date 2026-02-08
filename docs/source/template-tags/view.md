# call

The `view` template tag allows view functions to be called from within a template. More powerful than a simple `include` tag and quicker than a custom inclusion template tag.

```{note}
Make sure to [install `dj_angles`](../installation.md#template-tags) and include `{% load dj_angles %}` in your template if `"dj_angles.templatetags.dj_angles"` is not added to template built-ins.
```

## Example

```python
# www/urls.py
from django.urls import path

from www import views

app_name = "www"

urlpatterns = [
    path("index", views.index, name="index"),
    path("partial", views.partial, name="partial"),
]
```

```python
# www/views.py
from django.shortcuts import render
import uuid

def index(request):
    return render(request, "index.html", {})

def partial(request):
    random_uuid = uuid.uuid4()
    return render(request, "partial.html", {"random_uuid": random_uuid})
```

```html
<!-- www/templates/www/partial.html -->
<p>The uuid is {{ random_uuid }}</p>
```

### Import path

```html
<!-- www/templates/www/index.html -->
{% view 'www.views.partial' %}
```

### View name

```html
<!-- www/templates/www/index.html -->
{% view 'www:partial' %}
```
