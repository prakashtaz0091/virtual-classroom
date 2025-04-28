from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import PostAttachment

@receiver(pre_delete, sender=PostAttachment)
def delete_attachment_file(sender, instance, **kwargs):
    # Delete the file itself
    if instance.file:
        instance.file.delete(save=False)