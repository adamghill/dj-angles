from django.urls import re_path

from www import views

app_name = "www"

urlpatterns = [
    re_path(r".*", views.view),
]
