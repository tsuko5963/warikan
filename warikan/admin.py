from django.contrib import admin

# Register your models here.
from .models import HistoryModel, Account

class HistoryModelAdmin(admin.ModelAdmin):
    list_display = ["username", "date", "time"]
    search_fields = ["username"]

admin.site.register(HistoryModel, HistoryModelAdmin)
admin.site.register(Account)

