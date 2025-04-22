from django.shortcuts import render


def notes(request):
    return render(request, 'main/notes.html')


def submission_detail(request):
    return render(request, 'main/submission_detail.html')


def assignment_detail(request):
    return render(request, 'main/assignment_detail.html')


def classroom(request):
    return render(request, 'main/classroom.html')


def home(request):
    return render(request, 'main/home.html')