from django.contrib import admin

from .models import DateStorage


@admin.register(DateStorage)
class DateStorageAdmin(admin.ModelAdmin):
    pass
