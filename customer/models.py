from django.db import models
from workspace.models import Workspace
from product.models import *

# Create your models here.
class Customer(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='customers')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    profile_image = models.ImageField(blank=True, null=True, upload_to='profile_images/')
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(blank=True, null=True,)
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    gender = models.CharField(max_length=1, choices=gender_choices)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField()
    company = models.CharField(max_length=255)
    customer_type_choices = [
        ('student', 'Student'),
        ('client', 'Client')
    ]
    customer_type = models.CharField(max_length=10, choices=customer_type_choices)
    parents_name = models.CharField(max_length=100)
    parents_phone_no = models.CharField(max_length=15, blank=True, null=True)
    vat_pan_no = models.CharField(max_length=15, blank=True, null=True)
    ligal_document = models.FileField(blank=True, null=True, upload_to='ligal_document/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class Subscription(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='subscriptions')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='subscriptions')
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
class Sales(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sales')
    sales_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
class SalesDetail(models.Model):
    sales = models.ForeignKey(Sales, on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales_details')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.name} - {self.quantity} pcs'
