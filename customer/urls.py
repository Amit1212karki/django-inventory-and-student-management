from django.urls import path
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('students/',studentIndex, name='student-index'),
    path('clients/',clientIndex),
    path('add-student-record/',addStudent, name='add-student'),
    path('edit-student-record/<int:id>/',editStudent, name='edit-student'),
    path('update-student-record/<int:id>/',updateStudent, name='update-student'),
    path('delete-student-record/<int:id>/',deleteStudent, name='delete-student'),





]
