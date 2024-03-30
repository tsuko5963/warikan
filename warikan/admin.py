from django.contrib import admin

# Register your models here.
from .models import HistoryModel, Account

admin.site.register(HistoryModel)
admin.site.register(Account)

