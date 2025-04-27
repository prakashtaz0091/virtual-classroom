from django.shortcuts import render, redirect
from .import models
from django.contrib.auth.decorators import login_required
from .forms import ClassRoomForm
from common.decorators import teacher_required


@login_required
@teacher_required
def create_classroom(request):
    
    if request.method == 'POST':
        form = ClassRoomForm(request.POST, request.FILES)
        if form.is_valid():
            classroom = form.save(commit=False)
            classroom.teacher = request.user
            classroom.save()
            return redirect('home')
        else:
            return render(request, 'main/create_classroom.html', {'form': form})
    
    classroom_form = ClassRoomForm()
    context = {
        'form': classroom_form
    }
    return render(request, 'main/create_classroom.html', context)


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
def classroom(request, slug):    
    
    try:
        classroom = models.ClassRoom.objects.get(slug=slug)
    except models.ClassRoom.DoesNotExist:
        return redirect('home')
    
    context = {
        'classroom': classroom
    }
    
    return render(request, 'main/classroom.html', context)


@login_required
def home(request):
    
    all_classrooms = models.ClassRoom.objects.all()
    
    context = {
        'classrooms': all_classrooms
    }
    
    return render(request, 'main/home.html', context)