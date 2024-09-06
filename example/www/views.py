from django.http import Http404
from django.shortcuts import render


def view(request):
    path = request.path
    template_name = "index"

    if len(path) > 1 and path.startswith("/"):
        template_name = path[1:]

    if template_name == "favicon.ico":
        raise Http404()

    return render(request, f"www/{template_name}.html")
