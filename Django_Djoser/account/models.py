from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True
    )

    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'is_admin']

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.name
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_admin
    
    def has_module_perms(self, app_label):
        "does the user have permission to view the app `app_label`?"
        return True
    
    @property
    def is_staff(self):
        "IS the user a member of staff?"
        return self.is_admin