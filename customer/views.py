from django.shortcuts import render, redirect, get_object_or_404, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from workspace.models import Workspace
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.

def studentIndex(request):
    search_query = request.GET.get('search', '')  # Get search query or default to empty string

    students_list = Customer.objects.filter(customer_type='student')

    if search_query:
        students_list = students_list.filter(Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query) | Q(email__icontains=search_query))  # Filter based on search terms

    paginator = Paginator(students_list, 10)  # Show 10 students per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj, 'search_query': search_query}  # Add search query to context

    return render(request, 'dashboard/pages/students/index.html', context)

def clientIndex(request):
    clients = Customer.objects.filter(customer_type='client')
    return render(request, 'dashboard/pages/clients/index.html', {'clients': clients})

@login_required
def addStudent(request):
    if request.method == 'POST':
        try:
            Workspace_id = 1
            workspace = Workspace.objects.get(pk=Workspace_id)
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            image = None if not request.FILES.get('profile_image') else request.FILES.get('profile_image')
            email = request.POST.get('email')
            birth_date = None if not request.POST.get('date_of_birth') else request.POST.get('date_of_birth')
            gender = request.POST.get('gender')
            gender = request.POST.get('gender')
            phone = request.POST.get('phone')
            address = request.POST.get('address') 
            parents_name = request.POST.get('parents_name')
            parents_phone = request.POST.get('parents_phone')  
            document = None if not request.FILES.get('ligal_document') else request.FILES.get('ligal_document')

            new_student = Customer(
                first_name=first_name,
                last_name=last_name,
                profile_image=image,
                email=email,
                date_of_birth=birth_date,
                gender=gender,
                phone=phone,
                address=address,
                customer_type='student',
                workspace=workspace,
                parents_name=parents_name,
                parents_phone_no=parents_phone,
                ligal_document=document
            )
            new_student.save()
        except Exception as e:
           print(e)
           messages.error(request, 'An error occurred while saving the student.')
        return redirect('student-index')
    return render(request,'dashboard/pages/students/add.html')
    
def editStudent(request,id):
    editStudents =  get_object_or_404(Customer, customer_type='student', id=id)
    return render(request, 'dashboard/pages/students/edit.html', {'editStudent': editStudents})


def updateStudent(request, id):
    updateStudent = get_object_or_404(Customer, customer_type='student', id=id)

    if request.method == 'POST':
        updateStudent.first_name = request.POST.get('first_name')
        updateStudent.last_name = request.POST.get('last_name')
        if request.FILES.get('profile_image'):
            updateStudent.profile_image = request.FILES.get('profile_image')
        updateStudent.email = request.POST.get('email')
        updateStudent.date_of_birth = request.POST.get('date_of_birth')
        updateStudent.gender = request.POST.get('gender')
        updateStudent.phone = request.POST.get('phone')
        updateStudent.address = request.POST.get('address')
        updateStudent.parents_name = request.POST.get('parents_name')
        updateStudent.parents_phone_no = request.POST.get('parents_phone')
        if request.FILES.get('ligal_document'):
            updateStudent.ligal_document = request.FILES.get('profile_image')
        updateStudent.ligal_document = request.FILES.get('ligal_document')



        if not updateStudent.first_name or not updateStudent.last_name or not updateStudent.email or not updateStudent.date_of_birth or not updateStudent.gender or not updateStudent.phone or not updateStudent.address or not  updateStudent.parents_name or not  updateStudent.parents_phone_no or not  updateStudent.ligal_document:
            messages.error(request, 'Please fill in all the required fields.')
            return redirect('update-student', id=id)

        try:
            updateStudent.save()
            messages.success(request, 'Student updated successfully.')
            return redirect('student-index')
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
            return redirect('update-student', id=id)

    return render(request, 'dashboard/pages/students/edit.html', {'student': updateStudent})

def deleteStudent(request, id):
    deleteStudent = get_object_or_404(Customer,id=id)
    deleteStudent.delete()
    return redirect('student-index')
