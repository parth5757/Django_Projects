"""
Base core model.
"""
from django.db import models


class BaseModel(models.Model):
    """
    Base objects.
    """
    class Meta:
        abstract = True
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)