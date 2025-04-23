from django.shortcuts import render
from .import models

def notes(request):
    return render(request, 'main/notes.html')


def submission_detail(request):
    return render(request, 'main/submission_detail.html')


def assignment_detail(request):
    return render(request, 'main/assignment_detail.html')


def classroom(request):    
    return render(request, 'main/classroom.html')


def home(request):
    
    all_classrooms = models.ClassRoom.objects.all()
    
    context = {
        'classrooms': all_classrooms
    }
    
    return render(request, 'main/home.html', context)