from django.db import models
from app_modules.base.models import BaseModel
from django.utils.translation import gettext_lazy as _

from app_modules.company.models import Company

# Create your models here.
class Vendor(BaseModel):
    ACTIVE = "active"
    INACTIVE = "inactive"

    VENDOR_STATUS = (
        (ACTIVE, "Active"),
        (INACTIVE, "Inactive"),
    )
    address_line_1 = models.CharField(max_length=100, null=True, blank=True)
    address_line_2 = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    office_number_1 = models.CharField(max_length=50, null=True, blank=True)
    office_number_2 = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, null=True, blank=True)
    website = models.URLField(max_length=200, null=True, blank=True)
    status = models.CharField(_("Status"), max_length=10, choices=VENDOR_STATUS, default=ACTIVE)
    company = models.ForeignKey(Company, verbose_name=_("Company"), on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.email
    