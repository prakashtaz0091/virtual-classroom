from django.contrib import admin
from . import models


admin.site.register(models.ClassRoom)
admin.site.register(models.ClassroomMember)
admin.site.register(models.Assignment)
admin.site.register(models.AssignmentFile)
admin.site.register(models.Submission)
admin.site.register(models.SubmissionFile)
admin.site.register(models.Note)
admin.site.register(models.NoteFile)
admin.site.register(models.Post)
admin.site.register(models.Comment)