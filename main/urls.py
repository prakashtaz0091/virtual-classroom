from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # classroom
    path('classroom/create/', views.create_classroom, name='create_classroom'),
    path('classroom/<str:slug>/', views.classroom, name='classroom'),
    path('classroom/<str:slug>/join/', views.join_classroom, name='join_classroom'),
    
    # post
    path('trix-upload/', views.trix_upload, name='trix_upload'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<str:id>/update/', views.post_update, name='post-update'),
    path('post/<str:id>/delete/', views.post_delete, name='post-delete'),
    
    
    
    path('assignment/detail/', views.assignment_detail, name='assignment_detail'),
    
    path('submission/detail/', views.submission_detail, name='submission_detail'),
    
    path('notes/', views.notes, name='notes'),
]