from django.shortcuts import render, get_object_or_404
from customer.models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from product.models import *
from .models import *
import base64
from django.core.mail import EmailMessage
from django.http import JsonResponse
from datetime import datetime
from django.template.loader import render_to_string
from django.db.models import Sum

# Create your views here.
def index(request):
    sales_list = Sales.objects.all()
    sales_data = []

    for sales in sales_list:
        total_transactions = sales.transactions.aggregate(Sum('amount'))['amount__sum'] or 0
        pending_payment = sales.total - total_transactions
        sales_data.append({
            'sales': sales,
            'total_transactions': total_transactions,
            'pending_payment': pending_payment
        })

    return render(request, 'dashboard/pages/sales/index.html', {
        'sales_data': sales_data,
    })

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
        
        return JsonResponse({'message': 'Sales data saved successfully','sales_id': sales.id}, status=200)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
def view_sales_invoice(request, sales_id):
    sales = get_object_or_404(Sales, id=sales_id)
    sales_details = sales.details.all()
    transaction_details = sales.transactions.all()
    
    # Calculate total paid amount
    total_paid_amount = sales.transactions.aggregate(total_paid=Sum('amount')).get('total_paid') or 0
    
    # Calculate total due amount
    total_due_amount = sales.total - total_paid_amount
    
    return render(request, 'dashboard/pages/sales/view.html', {
        'sales': sales,
        'sales_details': sales_details,
        'transaction_details': transaction_details,
        'total_paid_amount': total_paid_amount,
        'total_due_amount': total_due_amount
    })

@csrf_exempt
def send_bill(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sales_id = data.get('sales_id')
            customer_email = data.get('email')
            
            # Fetch the sales data from the database
            sales = get_object_or_404(Sales, id=sales_id)
            sales_details = sales.details.all()
            transaction_details = sales.transactions.all()
            
            # Calculate total paid amount
            total_paid_amount = sales.transactions.aggregate(total_paid=Sum('amount')).get('total_paid') or 0
            
            # Calculate total due amount
            total_due_amount = sales.total - total_paid_amount
            
            # Use the email template, pass the sales and sales detail to email template and send the email
            context = {
                'sales': sales,
                'sales_details': sales_details,
                'transaction_details': transaction_details,
                'total_paid_amount': total_paid_amount,
                'total_due_amount': total_due_amount
            }
            
            # Render the email template with context
            email_body = render_to_string('email/bill_email_template.html', context)
            
            # Send email
            email = EmailMessage(
                subject='Your Bill',
                body=email_body,
                to=[customer_email],
            )
            email.content_subtype = 'html'  # Set the email content type to HTML
            email.send()
            
            # Update the sales object status to 'sent'
            sales.status = 'sent'
            sales.save()
            
            return JsonResponse({'message': 'Email sent successfully'}, status=200)
        except Exception as e:
            # Handle any potential errors and return an error response
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # Return a "Method Not Allowed" response for requests other than POST
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
def save_transaction(request,sales_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Extract data from the POST request
        transaction_amount = data.get('transaction_amount')
        transaction_date_str = data.get('transaction_date')
        transaction_payment_method = data.get('payment_method')
        transaction_notes = data.get('transaction_notes')
        sales = get_object_or_404(Sales, id=sales_id)

        
        try:
            transaction_date = datetime.strptime(transaction_date_str, '%Y-%m-%d').replace(tzinfo=timezone.get_current_timezone())
            # Save the transaction data to the database or perform other actions as needed
            # Example:
            transaction = Transaction(
                amount=transaction_amount,
                sales=sales,
                transaction_date=transaction_date,
                payment_method=transaction_payment_method,
                notes=transaction_notes
            )
            transaction.save()
            
            # Return a success response
            return JsonResponse({'message': 'Transaction saved successfully'}, status=200)
        except Exception as e:
            # Return an error response if an exception occurs
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # Return a "Method Not Allowed" response for requests other than POST
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
def show_template(request,sales_id):
    sales = get_object_or_404(Sales, id=sales_id)
    sales_details = sales.details.all()
    transaction_details = sales.transactions.all()
     # Calculate total paid amount
    total_paid_amount = sales.transactions.aggregate(total_paid=Sum('amount')).get('total_paid') or 0
    
    # Calculate total due amount
    total_due_amount = sales.total - total_paid_amount
    return render(request,'email/bill_email_template.html',{
        'sales': sales,
        'sales_details': sales_details,
        'transaction_details': transaction_details,
        'total_paid_amount': total_paid_amount,
        'total_due_amount': total_due_amount
    })