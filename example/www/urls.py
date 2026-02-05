from django.urls import path, re_path

from example.www import views

app_name = "www"

urlpatterns = [
    path("view_include", views.view_include, name="view_include"),
    re_path(r".*", views.view),
]
