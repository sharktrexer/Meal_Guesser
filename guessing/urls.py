from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("name_test/<name>", views.name_test, name="name_test"),
]