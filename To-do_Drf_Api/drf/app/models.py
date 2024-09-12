"""Models for app."""

from django.db import models
from django.urls import reverse
from core.models import BaseModel
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django_rest_passwordreset.signals import reset_password_token_created

class Student(BaseModel):
    """
    Student objects.
    """
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField()
    roll_number = models.IntegerField(default=0, unique=True)
    mobile = models.CharField(max_length=10, blank=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ('-created_at',)


class Todo(BaseModel):
    """
    Todo objects.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.TextField()
    tags = models.ManyToManyField('Tag')
    complete = models.BooleanField(default=False)
    complete_date = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.user.username

    class Meta:
        ordering = ('-created_at',)


class Tag(models.Model):
    """
    Tag objects.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


@receiver(reset_password_token_created)
def password_rest_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        "password Rest For {}".format("Swan"),
        email_plaintext_message,
        "noreply@somehost.local",
        [reset_password_token.user.email]
    )
