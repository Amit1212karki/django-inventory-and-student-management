from django.contrib import admin
from django import forms
from .models import *
# Register your models here.
class SubscriptionInline(admin.TabularInline):
    model = Subscription
    extra = 1  # Number of empty forms to display

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'email', 'phone','company', 'customer_type', 'created_at')
    inlines = [SubscriptionInline]


class SalesDetailInline(admin.TabularInline):
    model = SalesDetail
    extra = 1

class SalesAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'sales_date', 'status', 'created_at', 'updated_at')
    inlines = [SalesDetailInline]

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'product', 'start_date', 'end_date', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('customer__name', 'product__name')

admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Sales, SalesAdmin)
admin.site.register(SalesDetail)