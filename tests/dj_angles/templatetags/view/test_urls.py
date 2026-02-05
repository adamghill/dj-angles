from django.http import HttpResponse
from django.urls import path


def named_view(request):
    return HttpResponse("Named View")


def named_view_args(request, arg):
    return HttpResponse(f"Named View Arg: {arg}")


urlpatterns = [
    path("named/", named_view, name="named_view"),
    path("named/<str:arg>/", named_view_args, name="named_view_args"),
]
