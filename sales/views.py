from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'dashboard/pages/sales/index.html')

def addNewSales(request):
    return render(request,'dashboard/pages/sales/add.html')