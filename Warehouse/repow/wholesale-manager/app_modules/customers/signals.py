import contextlib
from django.db.models.signals import  post_save
from django.dispatch import receiver
from app_modules.customers.models import PriceLevel, PriceLevelProduct
from app_modules.product.models import Product
from django.http import JsonResponse


@receiver(post_save, sender=PriceLevel)
def save_price_level_product(sender, instance, **kwargs):

    with contextlib.suppress(Exception):
        price_level = instance
        company_id = instance.company.id

        products = Product.objects.filter(company=company_id)

        for product in products:

            if product.status == 'active':
                PriceLevelProduct.objects.create(price_level=price_level, product=product, custom_price=0)

                if product.box:
                    PriceLevelProduct.objects.create(price_level=price_level, product=product, unit_type='box', custom_price=0)

                if product.case:
                    PriceLevelProduct.objects.create(price_level=price_level, product=product, unit_type='case', custom_price=0)