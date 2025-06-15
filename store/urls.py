from . import views
from django.urls import path

urlpatterns = [
    path("", views.home, name="home"),
    path("product/<int:id>", views.details, name="details"),
    path("results", views.results, name="results"),
]