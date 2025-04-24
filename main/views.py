from django.shortcuts import render
from .import models
from django.contrib.auth.decorators import login_required


@login_required
def notes(request):
    return render(request, 'main/notes.html')


@login_required
def submission_detail(request):
    return render(request, 'main/submission_detail.html')


@login_required
def assignment_detail(request):
    return render(request, 'main/assignment_detail.html')


@login_required
def classroom(request):    
    return render(request, 'main/classroom.html')


@login_required
def home(request):
    
    all_classrooms = models.ClassRoom.objects.all()
    
    context = {
        'classrooms': all_classrooms
    }
    
    return render(request, 'main/home.html', context)