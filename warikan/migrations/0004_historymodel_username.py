# Generated by Django 5.0.2 on 2024-03-24 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warikan', '0003_alter_account_jaspay'),
    ]

    operations = [
        migrations.AddField(
            model_name='historymodel',
            name='username',
            field=models.CharField(default='', max_length=15),
        ),
    ]
