from django.contrib import admin
from django import forms
from .models import *
# Register your models here.
class SubscriptionInline(admin.TabularInline):
    model = Subscription
    extra = 1  # Number of empty forms to display

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone','company', 'created_at', 'updated_at')
    inlines = [SubscriptionInline]

class PurchaseDetailInlineForm(forms.ModelForm):
    class Meta:
        model = PurchaseDetail
        fields = ['product', 'quantity', 'price']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'product' in self.fields:
            self.fields['product'].widget.can_add_related = False  # Disable the add button for related products
            self.fields['product'].widget.can_change_related = False  # Disable the change link for related products

class PurchaseDetailInline(admin.TabularInline):
    model = PurchaseDetail
    form = PurchaseDetailInlineForm
    extra = 1  # Number of empty forms to display


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'purchase_date', 'status', 'created_at', 'updated_at')
    inlines = [PurchaseDetailInline]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.pk:
                # Calculate price for new instances
                instance.price = instance.product.price * instance.quantity
            instance.save()
        formset.save_m2m()

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'product', 'start_date', 'end_date', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('customer__name', 'product__name')

admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(PurchaseDetail)