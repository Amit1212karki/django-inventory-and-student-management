
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('',index),
    path('add-new-sales/',addNewSales), 
    path('store-sales-data/', store_sales_data),
] 
