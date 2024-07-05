from django.db import models
from app_modules.base.models import BaseModel
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your models here.

class Company(BaseModel):

    IS_ACTIVE = "active"
    IS_INACTIVE = "inactive"

    STATUS_TYPE = (
        (IS_ACTIVE,"Active"),
        (IS_INACTIVE,"Inactive"),
    )

    company_name = models.CharField(_('Company Name'),max_length=100)
    contact_person = models.CharField(_('Contact Person'),max_length=50)
    email = models.EmailField(_('Email'),unique=True)
    phone = models.CharField(_('Phone Number'),max_length=20, null=True, blank=True)
    status = models.CharField(_('Status'), choices=STATUS_TYPE, max_length=20, default=IS_ACTIVE)

    def __str__(self):
        return self.company_name
    
class Warehouse(BaseModel):

    IS_ACTIVE = "active"
    IS_INACTIVE = "inactive"

    STATUS_TYPE = (
        (IS_ACTIVE,"Active"),
        (IS_INACTIVE,"Inactive"),
    )

    name = models.CharField(_('Name'),max_length=100)
    address_line_1 = models.CharField(_('Address Line 1'),max_length=150, null=True, blank=True)
    address_line_2 = models.CharField(_('Address Line 2'),max_length=150, null=True, blank=True)
    city = models.CharField(_('City'),max_length=50, null=True, blank=True)
    state = models.CharField(_('State'),max_length=50, null=True, blank=True)
    zip_code = models.IntegerField(_('Zip Code'), null=True, blank=True)
    country = models.CharField(_('Country'),max_length=50, null=True, blank=True)
    latitude = models.CharField(_('Latitude'),max_length=50, null=True, blank=True)
    longitude = models.CharField(_('Longitude'),max_length=50, null=True, blank=True)
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True,related_name="warehouses")
    status = models.CharField(_('Status'), choices=STATUS_TYPE, max_length=20, default=IS_ACTIVE)

    def __str__(self):
        return self.name


class CompanyUsers(BaseModel):
    company = models.ForeignKey(Company, verbose_name=_("Company"), on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=_("Company"), on_delete=models.CASCADE, related_name="company_users")