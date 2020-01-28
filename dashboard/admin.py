from django.contrib import admin

from .models import Client, TimeSheet


class TimeSheetInlineAdmin(admin.TabularInline):
    model = TimeSheet

class ClientAdmin(admin.ModelAdmin):
    inlines = [TimeSheetInlineAdmin]

admin.site.register(Client, ClientAdmin)