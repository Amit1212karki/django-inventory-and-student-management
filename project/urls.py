
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('',index, name='login'),
    path('logout/',logout_view, name='logout'),
    path('dashboard/',dashboard, name='dashboard'),
    path('customer/',include('customer.urls')),
    path('product/',include('product.urls')),
    path('sales/',include('sales.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)