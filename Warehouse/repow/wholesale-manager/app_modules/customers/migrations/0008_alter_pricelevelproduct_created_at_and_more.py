# Generated by Django 4.1.7 on 2023-07-05 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0007_merge_20230704_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricelevelproduct',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='pricelevelproduct',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
