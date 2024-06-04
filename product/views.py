from django.shortcuts import render
from .models import *
# Create your views here.
def index(request):
    products = Product.objects.all()
    return render(request,'dashboard/pages/products/index.html',{'products':products})

def addProduct(request):
    return render(request,'dashboard/pages/products/add.html')