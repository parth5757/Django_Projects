from django.db import models
from django.core.validators import FileExtensionValidator
from app_modules.base.models import BaseModel
from app_modules.product.models import Product
from app_modules.company.models import Company
from app_modules.vendors.models import Vendor
from app_modules.purchase_order.validators import validate_invoice_file_extension
from django.utils.translation import gettext_lazy as _

class PurchaseOrder(BaseModel):
    
    COMPLETED = "completed"
    REVERTED = "reverted"
    PENDING = "pending"

    STATUS_CHOICES = (
        (COMPLETED, "Completed"),
        (REVERTED, "Reverted"),
        (PENDING, "Pending"),
    )
    company = models.ForeignKey(Company, verbose_name=_("Company"), on_delete=models.CASCADE, null=True, blank=True, related_name="company_purchase_order")
    vendor = models.ForeignKey(Vendor, verbose_name=_("Vendor"), on_delete=models.CASCADE, null=True, blank=True, related_name="vendor_purchase_order")
    bill_number = models.CharField(verbose_name=_("Bill No"), max_length=100)
    bill_date = models.DateField(verbose_name=_("Bill Date"))
    remarks = models.CharField(verbose_name=_("Remarks"), max_length=100, null=True, blank=True)
    total_price = models.FloatField(verbose_name=_("Total Price"), default=0.00)
    status = models.CharField(max_length=10, verbose_name=_("Status"), choices=STATUS_CHOICES, default=PENDING)
    invoice = models.FileField(verbose_name=_("Purchase Order Invoice"), upload_to="purchase-order-invoice", validators= [validate_invoice_file_extension], null=True, blank=True)

     

class PurchaseOrderProducts(BaseModel):
    
    purchase_order = models.ForeignKey(PurchaseOrder, verbose_name=_("Purchase Order"), on_delete=models.CASCADE ,null=True, related_name="purchase_order_products")
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True, related_name="products_purchase_order")
    unit_type = models.CharField(max_length=50, verbose_name=_('Unit Type'))
    quantity = models.PositiveIntegerField(verbose_name=_('Quantity'))
    total_pieces = models.PositiveIntegerField(verbose_name=_('Total Pieces'),default=0)  
    cost_price = models.FloatField(verbose_name=_("Cost Price"), default=0.00)


    def get_total_price(self):
        return f'{self.total_pieces * self.cost_price}'
    
    def get_unit_type_pieces(self):
        current_product = Product.objects.get(id=self.product.id)
        if(self.unit_type == 'Piece'):
            return f'1'
        elif(self.unit_type == 'Box'):
            return f'{current_product.box_piece}'
        elif(self.unit_type == 'Case'):
            return f'{current_product.case_piece}'


        