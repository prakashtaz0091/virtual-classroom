from django.db import models
from django.utils.text import slugify

class ClassRoom(models.Model):
    teacher = models.ForeignKey('account.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='classroom_covers', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
    
class ClassroomMember(models.Model):
    student = models.ForeignKey('account.User', on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='members')
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'classroom')
        
    def __str__(self):
        return f'{self.student.username} in {self.classroom.name}'   
    
    
    
class Assignment(models.Model):
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)     
    title = models.CharField(max_length=150)        
    description = models.TextField()
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    

class AssignmentFile(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    file = models.FileField(upload_to='assignment_files')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.assignment.title} file"
    
    

SUBMISSION_GRADES = (
    ('a+', 'A+'),
    ('a', 'A'),
    ('b+', 'B+'),
    ('b', 'B'),
    ('c+', 'C+'),
    ('c', 'C'),
    ('d+', 'D+'),
    ('d', 'D'),
    ('e', 'E'),
)

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey('account.User', on_delete=models.CASCADE)
    feedback = models.TextField(null=True, blank=True)
    grade = models.CharField(max_length=5, choices=SUBMISSION_GRADES, null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.assignment.title} submission"
    
    
class SubmissionFile(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    file = models.FileField(upload_to='submission_files')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.submission.assignment.title} file"
    
    
    
class Note(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    


class NoteFile(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    file = models.FileField(upload_to='note_files')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.note.title} file"
    
    
POST_TYPES = (
    ('post', 'Post'),
    ('announcement', 'Announcement'),
    ('classwork', 'Classwork'),
)

class Post(models.Model):
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, default="No title")
    type = models.CharField(max_length=20, choices=POST_TYPES, default='post')
    content = models.TextField()
    due_date = models.DateField(null=True, blank=True) # only for assignments/classwork
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.classroom.name} post"
    
 
class PostAttachment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='post_attachments')
    
    def __str__(self):
        return f"{self.post.title} attachment" 
    
 
   
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.post.classroom.name} comment"