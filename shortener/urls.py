from django.urls import path

from . import views

app_name = "shortener"

urlpatterns = [
    path("", views.index, name="index"),
    path("redirect/<str:short_code>/", views.redirect_url, name="redirect_url"),
    path("shorten/", views.shorten, name="shorten"),
    path("info/", views.info, name="info"),
]
