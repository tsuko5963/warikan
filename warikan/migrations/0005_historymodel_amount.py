# Generated by Django 5.0.2 on 2024-03-26 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warikan', '0004_historymodel_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='historymodel',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]