from background_task import background
from django.core.mail import send_mail


@background(schedule=0)  # Schedule to run after 5 seconds
def background_send_mail(subject, message, from_email, recipient_list):
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
    )
    # Your task logic here
    print("mail sent")
