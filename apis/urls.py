from django.urls import path
from . import views


urlpatterns = [
    path("class/all/", views.all_classes, name="all_classes"),
    path("teacher/all/", views.all_teachers, name="all_teachers"),
]
