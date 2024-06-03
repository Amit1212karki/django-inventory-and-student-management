from django.urls import path
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('students/',studentIndex),
    path('clients/',clientIndex),
    path('add-student-record/',addStudent),

]
