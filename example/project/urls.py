from django.urls import include, path
from www import urls as www_urls

urlpatterns = [
    path("", include(www_urls)),
]
