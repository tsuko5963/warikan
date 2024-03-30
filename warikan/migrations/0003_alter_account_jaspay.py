# Generated by Django 5.0.2 on 2024-03-04 03:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warikan', '0002_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='jaspay',
            field=models.CharField(max_length=10, validators=[django.core.validators.MinLengthValidator(10)]),
        ),
    ]
