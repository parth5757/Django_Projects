"""Admin interface for app."""

from app.models import *
from django.contrib import admin

admin.site.register(Student)
admin.site.register(Todo)
admin.site.register(Tag)