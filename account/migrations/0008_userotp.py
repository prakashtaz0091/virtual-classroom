# Generated by Django 5.2 on 2025-04-30 15:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_withdrawal_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserOTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.CharField(max_length=8)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_otp', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
