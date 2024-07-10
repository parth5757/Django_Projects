from django.contrib import admin
from account.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserModelAdmin(BaseUserAdmin):
    # the fields to used in displaying the User Model 
    # this fields ovrride a defination on base UserModelAdmin

    list_display = ('id', 'email', 'name', 'is_active', 'is_admin')
    list_filter = ('is_admin',)
    add_fieldsets = (
        (None,  {
            'classes': ('wide'),
            'fields': ('email', 'name', 'password1', 'password2'),
        })
    )

    search_fields = ('email',)
    ordering = ('email','id')
    filter_horizontal = ()


admin.site.register(User, UserModelAdmin)
    
    # fieldsets = (
    #     (None, {
    #         ('User Credentials', {'fields': ('email', 'password')}),
    #         ('Personal info', {'fields': ('name',)}),
    #         ('Permissions' {'fields': ('is_admin', 'is_active')}),
    #     }),
    # )