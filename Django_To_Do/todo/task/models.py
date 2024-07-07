from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class BaseModel(models.Model):
    class Meta:
        abstract = True

    id = models.AutoField(primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Task(BaseModel):
    task_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # task_slug = AutoSlugField(populate_from='task_name', unique=True, null=True, default=None)
    is_done = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.name)
    
    class Meta:
        ordering = ('created_at',)