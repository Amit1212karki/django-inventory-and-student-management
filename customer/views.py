from django.shortcuts import render
from .models import *
# Create your views here.

def studentIndex(request):
    students = Customer.objects.filter(customer_type='student')
    return render(request, 'dashboard/pages/students/index.html', {'students': students})

def clientIndex(request):
    clients = Customer.objects.filter(customer_type='client')
    return render(request, 'dashboard/pages/clients/index.html', {'clients': clients})

def addStudent(request):
    return render(request,'dashboard/pages/students/add.html')