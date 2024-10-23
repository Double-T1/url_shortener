from django.urls import path

from . import views

app_name = "shortener"

urlpatterns = [
    path("", views.index, name="index"),
    path("shorten/", views.shorten, name="shorten"),
    path("<str:short_url>/", views.redirect_url, name="redirect_url"),
]
