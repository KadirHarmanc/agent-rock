from django.urls import path

from accounts.views import my_profile


urlpatterns = [
    path("me/", my_profile),
]
