from django.db import models
from app_modules.base.models import BaseModel
from django.utils.translation import gettext_lazy as _
from app_modules.users.models import User
from app_modules.company.models import Company
import datetime
from app_modules.customers.validators import validate_file_extension
from app_modules.product.models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Customer(BaseModel):
    ACTIVE = "active"
    INACTIVE = "inactive"

    DISTRIBUTOR = "distributor"
    RETAIL = "retail"
    WHOLESALE = "wholesale"

    CASE = "case"
    CHECK = "check"
    NET_10 = "net 10"
    NET_15 = "net 15"
    NET_30 = "net 30"


    STATUS_CHOICES = (
        (ACTIVE,'Active'),
        (INACTIVE,'Inactive')
    )

    TYPE_CHOICES = (
        (DISTRIBUTOR,'Distributor'),
        (RETAIL,'Retail'),
        (WHOLESALE,'Wholesale')
    )

    TERM_CHOICES = (
        (CASE,'Case'),
        (CHECK,'Check'),
        (NET_10,'Net 10'),
        (NET_15, 'Net 15'),
        (NET_30, 'Net 30')
    )

    customer_name = models.CharField(_('Customer Name'), max_length=50)
    customer_type = models.CharField(_('Customer Type'), choices=TYPE_CHOICES, max_length=20)
    status = models.CharField(_('Status'), choices=STATUS_CHOICES, max_length=20)
    sales_rep = models.ForeignKey(User , on_delete= models.SET_NULL, null=True, blank=True)
    tax_id = models.CharField(_('Tax Id'), max_length=20, null=True, blank=True)
    terms = models.CharField(_('Terms'), choices=TERM_CHOICES, max_length=20)
    dba_name = models.CharField(_('DBA Name'), max_length=30, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="company", null=True, blank=True)
    document = models.FileField(upload_to='customer documents', validators=[validate_file_extension])
    store_open_time = models.TimeField(_('Store Open Time'), auto_now=False, auto_now_add=False)
    store_close_time = models.TimeField(_('Store Close Time'), auto_now=False, auto_now_add=False)

            # for billing address
    billing_address_line_1 = models.CharField(_('Address line 1'), max_length=100, null=True, blank=True)
    billing_address_line_2 = models.CharField(_('Address line 2'), max_length=100, null=True, blank=True)
    billing_suite_apartment = models.CharField(_('Suite/Apartment'), max_length=50, null=True, blank=True)
    billing_city = models.CharField(_('City'), max_length=20, null=True, blank=True)
    billing_state = models.CharField(_('State'), max_length=20, null=True, blank=True)
    billing_country = models.CharField(_('Country'), max_length=20, null=True, blank=True)
    billing_zip_code = models.IntegerField(_('Zip Code'))
    billing_latitude = models.FloatField(_('Latitude'), null=True, blank=True)
    billing_longitude = models.FloatField(_('Longitude'), null=True, blank=True)

            # for shipping address
    shipping_address_line_1 = models.CharField(_('Address line 1'), max_length=100, null=True, blank=True)
    shipping_address_line_2 = models.CharField(_('Address line 2'), max_length=100, null=True, blank=True)
    shipping_suite_apartment = models.CharField(_('Suite/Apartment'), max_length=50, null=True, blank=True)
    shipping_city = models.CharField(_('City'), max_length=20, null=True, blank=True)
    shipping_state = models.CharField(_('State'), max_length=20, null=True, blank=True)
    shipping_country = models.CharField(_('Country'), max_length=20, null=True, blank=True)
    shipping_zip_code = models.IntegerField(_('Zip Code'))
    shipping_latitude = models.FloatField(_('Latitude'), null=True, blank=True)
    shipping_longitude = models.FloatField(_('Longitude'), null=True, blank=True)

    def __str__(self):
        return self.customer_name
    
class MultipleContact(BaseModel):
    STORE = "store"
    MANAGER = "manager"
    EMPLOYEE = "employee"

    PERSON_TYPE_CHOICES = (
        (STORE,'Store'),
        (MANAGER,'Manager'),
        (EMPLOYEE,'Employee')
    )

    customer_obj = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer")
    type = models.CharField(_('Type'), max_length=20, choices=PERSON_TYPE_CHOICES)
    contact_person = models.CharField(_('Contact Person'), max_length=30)
    email = models.EmailField(_('Email'))
    mobile_no = models.CharField(_('Mobile No'), max_length=20, null=True, blank=True)
    is_default = models.BooleanField(_('is Default'), default=False)

    def __str__(self):
        return self.contact_person
    

class Payment(BaseModel):
    CHECK = "check"
    CASH = "cash"
    CREDIT_CARD = "credit card"
    MONEY_ORDER = "money order"
    ELECTRONIC_TRANSFER = "electronic transfer"

    PAYMENT_MODE_CHOICE = (
        (CHECK,'Check'),
        (CASH,'Cash'),
        (CREDIT_CARD,'Credit Card'),
        (MONEY_ORDER,'Money Order'),
        (ELECTRONIC_TRANSFER,'Electronic Transfer')
    )

    receive_date = models.DateField(_('Receive Date'),default=datetime.date.today)
    entry_date = models.DateField(_('Entry Date'),default=datetime.date.today)
    customer_name = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="payment_customer")
    receive_amount = models.FloatField(_('Receive Amount'), default=0.0)
    payment_mode = models.CharField(_('Payment Mode'), choices=PAYMENT_MODE_CHOICE , max_length=30)
    check_no = models.IntegerField(_('Check No'),  null=True, blank=True)
    reference_id = models.IntegerField(_('Reference Id'), null=True, blank=True)
    remark = models.CharField(_('Remark'), max_length=20, null=True, blank=True)

    def __str__(self):
        return self.customer_name
    

class SalesRoute(BaseModel):
    ACTIVE = "active"
    INACTIVE = "inactive"

    STATUS_CHOICES = (
        (ACTIVE,'Active'),
        (INACTIVE,'Inactive')
    )

    route_name = models.CharField(_('Route Name'), max_length=50)
    sales_rep = models.ForeignKey(User , on_delete= models.SET_NULL, null=True, blank=True, related_name="user")
    status = models.CharField(_('Status'), choices=STATUS_CHOICES, max_length=20)
    customer = models.ManyToManyField(Customer, null=True, blank=True, related_name="salesroute_customer")

    def __str__(self):
        return self.route_name
    
    
class PriceLevel(BaseModel):
    ACTIVE = "active"
    INACTIVE = "inactive"

    DISTRIBUTOR = "distributor"
    RETAIL = "retail"
    WHOLESALE = "wholesale"

    STATUS_CHOICES = (
        (ACTIVE,'Active'),
        (INACTIVE,'Inactive')
    )

    TYPE_CHOICES = (
        (DISTRIBUTOR,'Distributor'),
        (RETAIL,'Retail'),
        (WHOLESALE,'Wholesale')
    )


    customer_type = models.CharField(_('Customer Type'), choices=TYPE_CHOICES, max_length=20)
    price_level = models.CharField(_('Price Level Name'), max_length=30)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="company_pricelevel", null=True, blank=True)
    status = models.CharField(_('Status'), choices=STATUS_CHOICES, max_length=20)

    def __str__(self):
        return self.price_level
    
class PriceLevelProduct(BaseModel):

    BOX = "box"
    CASE = "case"
    PIECE = "piece"

    UNIT_TYPES_CHOICES = (
        (BOX, 'Box'),
        (CASE, 'Case'),
        (PIECE, 'Piece'),
    )

    price_level = models.ForeignKey(PriceLevel, on_delete=models.CASCADE, related_name="pricelevel")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product")
    unit_type = models.CharField(_('Unit Type'), choices=UNIT_TYPES_CHOICES, max_length=7, default=PIECE)
    custom_price = models.PositiveIntegerField(_('Custom Price'))

    def __str__(self):
        return self.id
    
