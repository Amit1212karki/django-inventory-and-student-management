from django.urls import path
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('',index, name='product-index'),
    path('add-product/',addProduct, name='add-product'),
    path('edit-product/<int:id>/',editProduct, name='edit-product'),
    path('update-product/<int:id>/',updateProduct, name='update-product'),
    path('delete-product/<int:id>/',deleteProduct, name='delete-product')


]
