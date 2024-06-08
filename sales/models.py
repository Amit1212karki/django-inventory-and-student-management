from django.db import models
from product.models import *
from customer.models  import *
from django.utils import timezone
# Create your models here.

class Sales(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sales')
    sales_date = models.DateTimeField(default=timezone.now)  # Set the default value to the current datetime
    status = models.CharField(max_length=50, choices=[
        ('draft', 'Draft'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ], default='draft')
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    vat_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True)
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
class SalesDetail(models.Model):
    sales = models.ForeignKey(Sales, on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales_details')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.name} - {self.quantity} pcs'
    

class Transaction(models.Model):
    sales = models.ForeignKey(Sales, on_delete=models.CASCADE, related_name='transactions')
    transaction_date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[
        ('cash', 'Cash'),
        ('esewa', 'Esewa'),
        ('bank_transfer', 'Bank Transfer'),
        ('other', 'Other'),
    ])
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Transaction for Sales ID: {self.sales.id}"