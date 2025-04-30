from django.contrib import admin
from . import models

admin.site.register(models.User)
admin.site.register(models.Profile)
admin.site.register(models.Withdrawal)
admin.site.register(models.UserOTP)
