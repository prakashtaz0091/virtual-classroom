from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('classroom/', views.classroom, name='classroom'),
    path('assignment/detail/', views.assignment_detail, name='assignment_detail'),
    path('submission/detail/', views.submission_detail, name='submission_detail'),
    path('notes/', views.notes, name='notes'),
]