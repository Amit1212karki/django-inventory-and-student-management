from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from sales.models import *
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from collections import OrderedDict
import calendar
import json
from decimal import Decimal
import datetime
from datetime import timedelta
from django.utils import timezone


def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to dashboard page
            return redirect('/dashboard/')
        else:
            error_message = "Invalid email or password."
            return render(request, 'auth/login.html', {'error_message': error_message})
    else:
        return render(request, 'auth/login.html')
    
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

@login_required
def dashboard(request):
    now = timezone.now()
    one_week_ago = now - timedelta(days=7)
    
    new_customers_count = Customer.objects.filter(created_at__gte=one_week_ago).count()
    total_sales_decimal = Sales.objects.aggregate(total=Sum('total'))['total'] or Decimal('0.00')
    total_transaction_decimal = Transaction.objects.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    total_sales = round(float(total_sales_decimal), 2)
    total_transaction = round(float(total_transaction_decimal), 2)
    total_pending_amount = total_sales - total_transaction

    # Aggregate sales data by month
    monthly_sales = Sales.objects.annotate(month=TruncMonth('sales_date')).values('month').annotate(total=Sum('total')).order_by('month')

    # Prepare data for the chart
    sales_dict = OrderedDict()
    for sale in monthly_sales:
        month_str = sale['month'].strftime("%b")  # Format date as month abbreviation
        sales_dict[month_str] = sale['total']
    
    # Ensure all months are represented in the sales_dict even if no sales were made
    for month_num in range(1, 13):
        month_str = calendar.month_abbr[month_num]
        if month_str not in sales_dict:
            sales_dict[month_str] = 0

    sales_values = list(sales_dict.values())
    sales_categories = list(sales_dict.keys())

    # Convert sales_values and sales_categories to list of dictionaries
    sales_data_json = []
    for i in range(len(sales_values)):
        sales_data_json.append({'sales': sales_values[i], 'month': sales_categories[i]})

    # Use the custom JSON encoder to serialize sales_data_json
    sales_data_json_str = json.dumps(sales_data_json, cls=DecimalEncoder)

    monthly_transactions = Transaction.objects.annotate(month=TruncMonth('transaction_date')).values('month').annotate(total=Sum('amount')).order_by('month')

    transaction_dict = OrderedDict()
    for transaction in monthly_transactions:
        month_str = transaction['month'].strftime("%b")  # Format date as month abbreviation
        transaction_dict[month_str] = transaction['total']
    
    for month_num in range(1, 13):
        month_str = calendar.month_abbr[month_num]
        if month_str not in transaction_dict:
            transaction_dict[month_str] = 0

    transaction_values = list(transaction_dict.values())
    transaction_categories = list(transaction_dict.keys())

    transaction_data_json = []
    for i in range(len(transaction_values)):
        transaction_data_json.append({'transactions': transaction_values[i], 'month': transaction_categories[i]})

    transaction_data_json_str = json.dumps(transaction_data_json, cls=DecimalEncoder)


    top_products = SalesDetail.objects.values('product__name').annotate(total_sales=Sum('total')).order_by('-total_sales')[:5]
    top_products_dict = OrderedDict()
    for product in top_products:
        top_products_dict[product['product__name']] = product['total_sales']

    top_products_labels = list(top_products_dict.keys())
    top_products_values = list(top_products_dict.values())

    top_products_data_json = json.dumps({'labels': top_products_labels, 'values': top_products_values}, cls=DecimalEncoder)

    context = {
        'total_sales': total_sales,
        'total_transaction': total_transaction,
        'total_pending_amount': total_pending_amount,
        'sales_data': sales_data_json_str, 
        'transaction_data': transaction_data_json_str, 
        'top_products_data' : top_products_data_json,
        'new_customers' : new_customers_count,
    }

    return render(request, 'dashboard/pages/index.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')