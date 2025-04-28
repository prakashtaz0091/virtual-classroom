from django.shortcuts import render, redirect
from .import models
from django.contrib.auth.decorators import login_required
from .forms import ClassRoomForm
from common.decorators import teacher_required
from django.http import JsonResponse
from django.contrib import messages
from django.core.files.storage import default_storage
from django.conf import settings
import os
import uuid
from datetime import datetime


def trix_upload(request):
    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]

        # Check file size (optional)
        max_size_mb = 5  # Limit to 5 MB
        if uploaded_file.size > max_size_mb * 1024 * 1024:
            return JsonResponse({"error": "File too large. Max size is 5MB."}, status=400)

        # Validate file type
        allowed_types = [
            'image/jpeg', 'image/png', 'image/gif',
            'application/pdf',
        ]
        if uploaded_file.content_type not in allowed_types:
            return JsonResponse({"error": "Invalid file type."}, status=400)

        # Get file extension
        _, file_extension = os.path.splitext(uploaded_file.name)

        # Generate unique filename
        unique_filename = f"{uuid.uuid4().hex}{file_extension}"

        # Optional: Organize uploads by date
        today = datetime.now().strftime('%Y/%m/%d')
        save_path = os.path.join("trix_uploads", today, unique_filename)

        # Save the file
        path = default_storage.save(save_path, uploaded_file)

        # Build full file URL
        file_url = settings.MEDIA_URL + path

        return JsonResponse({"url": file_url})

    return JsonResponse({"error": "Invalid request"}, status=400)


@teacher_required
def post_update(request, id):
    pass


@teacher_required
def post_delete(request, id):
    pass


@teacher_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        slug = request.POST.get('slug')
        attachment = request.FILES.get('attachment')
        post_type = request.POST.get('post_type')
        
        
        if not title or not content:
            messages.error(request, "Title and content are required.")
            return redirect('classroom', slug=slug)

        post = models.Post(
            title=title,
            type = post_type,
            content=content,
            classroom=models.ClassRoom.objects.get(slug=slug)
        )
                
        if post_type == 'classwork':
            due_date = request.POST.get('due_date')
            post.due_date = due_date

        post.save()

        if attachment:
            models.PostAttachment.objects.create(post=post, file=attachment)

        messages.success(request, "Post created successfully!")
        

    return redirect('classroom', slug=request.POST.get('slug'))



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



def notes(request):
    return render(request, 'main/notes.html')



def submission_detail(request):
    return render(request, 'main/submission_detail.html')



def assignment_detail(request):
    return render(request, 'main/assignment_detail.html')



def classroom(request, slug):    
    
    try:
        classroom = models.ClassRoom.objects.get(slug=slug)
        posts = models.Post.objects.filter(classroom=classroom).order_by('-updated_at')
    except models.ClassRoom.DoesNotExist:
        return redirect('home')
    
    context = {
        'classroom': classroom,
        'slug': slug,
        'posts': posts
    }
    
    return render(request, 'main/classroom.html', context)



def home(request):
    
    all_classrooms = models.ClassRoom.objects.all()
    
    context = {
        'classrooms': all_classrooms
    }
    
    return render(request, 'main/home.html', context)