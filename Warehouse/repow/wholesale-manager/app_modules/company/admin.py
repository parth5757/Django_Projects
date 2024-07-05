from django.contrib import admin
from app_modules.company.models import Company, Warehouse, CompanyUsers

admin.site.register(Company)
admin.site.register(Warehouse)
admin.site.register(CompanyUsers)