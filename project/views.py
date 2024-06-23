from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from sales.models import *
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from collections import OrderedDict
import calendar
import json
from decimal import Decimal
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
        return render(request, 'auth/login.html')@login_required
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

@login_required
def dashboard(request):
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

    context = {
        'total_sales': total_sales,
        'total_transaction': total_transaction,
        'total_pending_amount': total_pending_amount,
        'sales_data': sales_data_json_str,  # Convert to JSON format using custom encoder
    }

    return render(request, 'dashboard/pages/index.html', context)