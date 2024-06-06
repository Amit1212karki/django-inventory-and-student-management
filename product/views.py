from django.shortcuts import render, redirect, get_object_or_404
from .models import *
# Create your views here.
def index(request):
    products = Product.objects.all()
    return render(request,'dashboard/pages/products/index.html',{'products':products})

def addProduct(request):
    if request.method == 'POST':
        workspace_id = 1
        workspace = Workspace.objects.get(pk=workspace_id)
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        product_image = None if not request.FILES.get('product_image') else request.FILES.get('product_image')
        product_file = None if not request.FILES.get('product_file') else request.FILES.get('product_file')
        inventory_count = request.POST.get('inventory_count')
        is_recurring = request.POST.get('isRecurring')
        recurring_period = request.POST.get('recurringPeriod') if is_recurring == 'True' else None
        description = request.POST.get('description')

        product = Product(
            workspace=workspace,
            name=product_name,
            price=product_price,
            inventory_count=inventory_count,
            isrecurring='Y' if is_recurring == 'True' else 'N',
            subscription_period=recurring_period,
            description=description,
            image=product_image,
            file=product_file
        )
        product.save()
        return redirect('add-product') 

       
    return render(request,'dashboard/pages/products/add.html')


def editProduct(request,id):
    editProducts = get_object_or_404(Product, id=id)
    return render(request, 'dashboard/pages/products/edit.html', {'editProduct': editProducts})


def updateProduct(request, id):
     if request.method == 'POST':
        updateProduct = get_object_or_404(Product, id=id)

        updateProduct.name = request.POST.get('product_name')
        updateProduct.price = request.POST.get('product_price')
        updateProduct.description = request.POST.get('description')
        updateProduct.inventory_count = request.POST.get('inventory_count')
        updateProduct.isrecurring = request.POST.get('isRecurring')
        updateProduct.subscription_period = request.POST.get('recurringPeriod') if  updateProduct.isrecurring == 'True' else None
        updateProduct.image = None if not request.FILES.get('product_image') else request.FILES.get('product_image')
        updateProduct.file = None if not request.FILES.get('product_file') else request.FILES.get('product_file')
        if updateProduct.isrecurring == 'True':
            updateProduct.subscription_period = request.POST.get('recurringPeriod')
        else:
             updateProduct.subscription_period = None

        updateProduct.save()
        return redirect('produt-index')
     
     return render(request, 'dashboard/pages/products/edit.html', {'updateProducts': updateProduct}) 