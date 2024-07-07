from django import forms
from .models import Task

class TaskFrom(forms.ModelFOrm):
    class Meta:
        model = Task
        fields = ['task_name', 'user']