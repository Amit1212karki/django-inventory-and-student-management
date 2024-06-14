from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.
def index(request):

    product_search_query = request.GET.get('search', '')  # Get search query or default to empty string
    all_products = Product.objects.all().order_by('-created_at')
    if product_search_query:
        products = all_products.filter(Q(name__icontains=product_search_query) | Q(price__icontains=product_search_query))
    else:
        products = all_products
        
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)
     
    context = {'products': page_obj, 'search_query': product_search_query}
    return render(request,'dashboard/pages/products/index.html', context)

def addProduct(request):
    if request.method == 'POST':
        workspace_id = 1
        workspace = Workspace.objects.get(pk=workspace_id)
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        product_image = None if not request.FILES.get('product_image') else request.FILES.get('product_image')
        product_file = None if not request.FILES.get('product_file') else request.FILES.get('product_file')
        inventory_count = None if not request.POST.get('inventory_count') else request.POST.get('inventory_count')
        is_recurring = request.POST.get('isRecurring')
        recurring_period = request.POST.get('recurringPeriod') if is_recurring == 'True' else None
        description = request.POST.get('description')

        product = Product(
            workspace=workspace,
            name=product_name,
            price=product_price,
            inventory_count=inventory_count,
            isrecurring='Y' if is_recurring == 'True' else 'N',
            recurring_period=recurring_period,
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
    updateProduct = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        updateProduct.name = request.POST.get('product_name')
        updateProduct.price = request.POST.get('product_price')
        updateProduct.description = request.POST.get('description')
        updateProduct.inventory_count = None if not request.POST.get('inventory_count') else request.POST.get('inventory_count')
        updateProduct.recurring_period = request.POST.get('recurringPeriod') if  updateProduct.isrecurring == 'True' else None
        updateProduct.image = None if not request.FILES.get('product_image') else request.FILES.get('product_image')
        updateProduct.file = None if not request.FILES.get('product_file') else request.FILES.get('product_file')
        is_recurring = request.POST.get('isRecurring')

        updateProduct.isrecurring = 'Y' if is_recurring == 'True' else 'N'
        if updateProduct.isrecurring == 'Y':
            updateProduct.recurring_period = request.POST.get('recurringPeriod')
        else:
            updateProduct.recurring_period = None


        updateProduct.save()
        return redirect('product-index')
     
    return render(request, 'dashboard/pages/products/edit.html', {'updateProducts': updateProduct}) 

def deleteProduct(request, id):
    if request.method == 'POST':
        deleteProduct = get_object_or_404(Product, id=id)
        deleteProduct.delete()
        return redirect('product-index')
    
    return redirect('product-index')

        