from django.db import models
from django.contrib.auth.models import AbstractUser
from app_modules.base.models import BaseModel
from django.utils.translation import gettext_lazy as _


# Create your models here.
class User(AbstractUser, BaseModel):
    SUPER_ADMIN = "super admin"
    ADMIN = "admin"
    COMPANY_ADMIN = "company admin"
    SALES_REPRESENTATIVE = "sales representative"
    DRIVER = "driver"

    USER_ROLE = (
        (SUPER_ADMIN, "Super Admin"),
        # (ADMIN, "Admin"),
        (COMPANY_ADMIN, "Company Admin"),
        (SALES_REPRESENTATIVE, "Sales Representative"),
        (DRIVER, "Driver"),
    )
    email = models.EmailField(_('Email'), unique=True)
    full_name = models.CharField(_('Full Name'), max_length=20, null=True, blank=True)
    phone = models.CharField(_('Phone'), max_length=20, null=True, blank=True)
    role = models.CharField(_('Role'), choices=USER_ROLE, max_length=20, default=ADMIN)

    @property
    def company(self):    # sourcery skip: assign-if-exp, reintroduce-else
        company_user = self.company_users.first()
        if company_user:
            return company_user.company.company_name
        return None
    
    @property
    def get_company_id(self):    # sourcery skip: assign-if-exp, reintroduce-else
        company_user = self.company_users.first()
        if company_user:
            return company_user.company.id
        return None