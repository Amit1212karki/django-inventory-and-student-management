from django.shortcuts import render
from customer.models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from product.models import *
from .models import *

# Create your views here.
def index(request):
    return render(request,'dashboard/pages/sales/index.html')

def addNewSales(request):
    customers = Customer.objects.all()
    products = Product.objects.all()

    # Pass the customers and products to the template
    context = {
        'customers': customers,
        'products': products,
    }
    return render(request, 'dashboard/pages/sales/add.html', context)

@csrf_exempt  # You may need to disable CSRF protection for this view if you're sending requests from another domain
def store_sales_data(request):
    if request.method == 'POST':
        # Parse the JSON data sent by Axios
        data = json.loads(request.body)
        
        # Extract data from the JSON
        customer_id = data.get('customer_id')
        sales_date = data.get('date')
        status = data.get('status')
        sub_total = data.get('sub_total')
        total = data.get('total')
        discount = data.get('discount')
        vat_percent = data.get('vat_percent')
        vat_amount = data.get('vat_amount')
        sales_details = data.get('sales_details', [])
        
        # Save Sales object
        sales = Sales.objects.create(
            customer_id=customer_id,
            sales_date=sales_date,
            status=status,
            sub_total=sub_total,
            total=total,
            discount=discount,
            vat_percent=vat_percent,
            vat_amount=vat_amount
        )
        
        # Save SalesDetail objects
        for detail in sales_details:
            SalesDetail.objects.create(
                sales=sales,
                product_id=detail.get('product_id'),
                quantity=detail.get('quantity'),
                price=detail.get('price'),
                total=detail.get('total')
            )
        
        return JsonResponse({'message': 'Sales data saved successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)