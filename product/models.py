from django.db import models
from workspace.models import Workspace
# Create your models here.
class Product(models.Model):
    SUBSCRIPTION_PERIOD_CHOICES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory_count = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    is_subscription = models.BooleanField(default=True)
    subscription_period = models.CharField(max_length=50, choices=SUBSCRIPTION_PERIOD_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.FileField(upload_to='product_images/', blank=True, null=True)
    file = models.FileField(upload_to='product_files/', blank=True, null=True)

    def __str__(self):
        return self.name
    
