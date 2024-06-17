from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from sales.models import *
from django.db.models import Sum


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
@login_required
def dashboard(request):
    total_sales = Sales.objects.aggregate(total=Sum('total'))['total'] or 0
    total_transaction = Transaction.objects.aggregate(total=Sum('amount'))['total'] or 0


    total_sales = round(total_sales, 2)
    total_transaction = round(total_transaction, 2)
    total_pending_amount  = total_sales - total_transaction


    context = {
    'total_sales': total_sales,
    'total_transaction':total_transaction,
    'total_pending_amount':total_pending_amount

    }

    return render(request,'dashboard/pages/index.html',context)