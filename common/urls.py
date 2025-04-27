from django.urls import path
from .import views

urlpatterns = [
    path('not-authorized/', views.not_authorized, name='not_authorized'),
]