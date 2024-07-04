from django.db import models
from django.core.validators import validate_email
from django.contrib.auth.models import AbstractUser


# class CustomUser(AbstractUser):
#     # Add custom fields if needed
#     pass

class Teacher(models.Model):
    name = models.CharField(max_length=70)
    email = models.EmailField(max_length=100, validators=[validate_email])
    password = models.CharField(max_length=100)
    is_teacher = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

class User(models.Model):
    name = models.CharField(max_length=70)
    email = models.EmailField(max_length=100, validators=[validate_email])
    password = models.CharField(max_length=100)
    is_student = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)