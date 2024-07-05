from django.contrib import admin
from app_modules.customers.models import Customer, Payment

# Register your models here.
admin.site.register(Customer)
admin.site.register(Payment)