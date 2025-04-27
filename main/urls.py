from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # classroom
    path('classroom/create/', views.create_classroom, name='create_classroom'),
    path('classroom/<str:slug>/', views.classroom, name='classroom'),
    
    
    path('assignment/detail/', views.assignment_detail, name='assignment_detail'),
    
    path('submission/detail/', views.submission_detail, name='submission_detail'),
    
    path('notes/', views.notes, name='notes'),
]