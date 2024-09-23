from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("rand_meal", views.rand_meal, name="rand_meal"),
    path("end", views.ending, name="ending")
]