
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('',index),
    path('add-new-sales/',addNewSales), 
    path('store-sales-data/', store_sales_data),
    path('view-sales-invoice/<int:sales_id>/', view_sales_invoice),
    path('send-bill/', send_bill),
    path('save-transaction/<int:sales_id>', save_transaction),
    path('email-temp/<int:sales_id>', show_template),




] 
