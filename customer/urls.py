from django.urls import path
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('students/', studentIndex, name='student-index'),
    path('add-student-record/', addStudent, name='add-student'),
    path('edit-student-record/<int:id>/', editStudent, name='edit-student'),
    path('update-student-record/<int:id>/', updateStudent, name='update-student'),
    path('delete-student-record/<int:id>/', deleteStudent, name='delete-student'),

    path('clients/', clientIndex, name='client-index'),
    path('add-clients-record/', addClient, name='add-client'),
    path('edit-clients-record/<int:id>/', editClient, name='edit-client'),
    path('update-clients-record/<int:id>/', updateClient, name='update-client'),
    path('delete-clients-record/<int:id>/', deleteClient, name='delete-client'),



]
