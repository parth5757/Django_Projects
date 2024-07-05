from django.contrib import admin
from app_modules.product.models import Category,SubCategory,Brand,Product,WarehouseProductStock,WarehouseProductStockHistory

# Register your models here.

admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(WarehouseProductStock)
admin.site.register(WarehouseProductStockHistory)

