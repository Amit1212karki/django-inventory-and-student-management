from django.contrib import admin
from .models import *
# Register your models here.

class SalesDetailInline(admin.TabularInline):
    model = SalesDetail
    extra = 1

class SalesAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'sales_date', 'status', 'created_at', 'updated_at')
    inlines = [SalesDetailInline]

admin.site.register(Sales, SalesAdmin)
admin.site.register(SalesDetail)
admin.site.register(Transaction)
