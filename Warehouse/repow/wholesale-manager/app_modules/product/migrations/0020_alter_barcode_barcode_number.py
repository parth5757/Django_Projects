# Generated by Django 4.1.7 on 2023-07-05 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0019_barcode_product_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barcode',
            name='barcode_number',
            field=models.BigIntegerField(),
        ),
    ]
