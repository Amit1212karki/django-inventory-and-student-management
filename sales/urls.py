
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('',index, name='sales-index'),
    path('add-new-sales/',addNewSales), 
    path('store-sales-data/', store_sales_data),
    path('edit-sales-data/<int:sales_id>', edit_sales, name='edit-sales'),
    path('update-sales-data/<int:sales_id>/', update_sales_data, name='update-sales-data'),
    path('delete-sales-data/<int:sales_id>/', delete_sales, name='delete-sales-data'),
    path('view-sales-invoice/<int:sales_id>/', view_sales_invoice),
    path('send-bill/', send_bill),
    path('save-transaction/<int:sales_id>/', save_transaction),
    path('email-temp/<int:sales_id>/', show_template),


    path('transaction-index/', transactionIndex, name='transaction-index')


] 



