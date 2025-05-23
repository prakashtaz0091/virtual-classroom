from django.db import models
from django.contrib.auth.models import AbstractUser

USER_ROLES = (("student", "Student"), ("teacher", "Teacher"))


class User(AbstractUser):
    role = models.CharField(max_length=20, choices=USER_ROLES, default="student")
    is_verified = models.BooleanField(default=False)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)
    avatar = models.ImageField(default="default.jpg", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} Profile"


WITHDRAWAL_STATUS = (
    ("requested", "Requested"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
)


class Withdrawal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="withdrawals")
    amount = models.FloatField()
    status = models.CharField(
        max_length=20, choices=WITHDRAWAL_STATUS, default="requested"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} withdrawal"


class UserOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_otp")
    otp = models.CharField(max_length=8)
    new_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} OTP"
