from django.shortcuts import render
from customer.models import *
from product.models import *

# Create your views here.
def index(request):
    return render(request,'dashboard/pages/sales/index.html',)

def addNewSales(request):
    customers = Customer.objects.all()
    products = Product.objects.all()

    # Pass the customers and products to the template
    context = {
        'customers': customers,
        'products': products,
    }
    return render(request, 'dashboard/pages/sales/add.html', context)