# Generated by Django 4.1.10 on 2024-01-23 06:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enroll', '0002_alter_user_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('email', models.EmailField(max_length=100, validators=[django.core.validators.EmailValidator()])),
                ('password', models.CharField(max_length=100)),
            ],
        ),
    ]