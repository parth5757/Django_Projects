from django.contrib import admin
from .models import Category, Server, Channel

admin.site.register(Channel)
admin.site.register(Server)
admin.site.register(Category)