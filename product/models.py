from django.db import models
from workspace.models import Workspace
from django.core.files.storage import FileSystemStorage
# Create your models here.
class Product(models.Model):
    RECURRING_PERIOD_CHOICES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]
    isrecurring_choices = [
        ('Y', 'Yes'),
        ('N', 'No')
    ]
    isrecurring = models.CharField(max_length=1, choices=isrecurring_choices, default='N')
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory_count = models.PositiveIntegerField(blank=True, null=True, default=0)
    is_available = models.BooleanField(default=True)
    recurring_period = models.CharField(max_length=50, choices=RECURRING_PERIOD_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.FileField(upload_to='product_images/', blank=True, null=True)
    file = models.FileField(upload_to='product_files/', blank=True, null=True)

    def __str__(self):
        return self.name
    
