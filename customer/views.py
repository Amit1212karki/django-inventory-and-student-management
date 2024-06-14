from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from workspace.models import Workspace
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.

def studentIndex(request):
    search_query = request.GET.get('search', '')  # Get search query or default to empty string

    students_list = Customer.objects.filter(customer_type='student').order_by('-created_at')

    if search_query:
        students_list = students_list.filter(Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query) | Q(email__icontains=search_query))  # Filter based on search terms

    paginator = Paginator(students_list, 10)  # Show 10 students per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj, 'search_query': search_query}  # Add search query to context

    return render(request, 'dashboard/pages/students/index.html', context)

def clientIndex(request):
    clients = Customer.objects.filter(customer_type='client').order_by('-created_at')
    client_search_query = request.GET.get('search', '')

    if client_search_query:
        clients = clients.filter(Q(first_name__icontains=client_search_query) | Q(last_name__icontains=client_search_query) | Q(email__icontains=client_search_query) | Q(company__icontains=client_search_query) | Q(vat_pan_no__icontains=client_search_query) | Q(phone__icontains=client_search_query))
    else:
        clients = clients
    paginator = Paginator(clients, 10)  # Show 10 students per page

    page_number = request.GET.get('page')
    client_with_paginator = paginator.get_page(page_number)

    context = {'clients': client_with_paginator, 'search_query': client_search_query} 
    return render(request, 'dashboard/pages/clients/index.html', context)

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
            phone = request.POST.get('phone')
            address = request.POST.get('address') 
            parents_name = request.POST.get('parents_name')
            parents_phone = request.POST.get('parents_phone')  
            document = None if not request.FILES.get('legal_document') else request.FILES.get('legal_document')

            if not first_name or not last_name or not email or not gender or not phone or not address or not parents_name or not parents_phone:
                messages.error(request, 'Please fill in all the required fields.')
                return redirect('add-student')
            
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
                legal_document=document
            )
            new_student.save()
        except Exception as e:
           print(e)
           messages.error(request, 'An error occurred while saving the student.')
        return redirect('add-student')
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
        if request.POST.get('date_of_birth'):
             updateStudent.date_of_birth = request.POST.get('date_of_birth')
        updateStudent.gender = request.POST.get('gender')
        updateStudent.phone = request.POST.get('phone')
        updateStudent.address = request.POST.get('address')
        updateStudent.parents_name = request.POST.get('parents_name')
        updateStudent.parents_phone_no = request.POST.get('parents_phone')
        if request.FILES.get('legal_document'):
            updateStudent.legal_document = request.FILES.get('legal_document')

        if not updateStudent.first_name or not updateStudent.last_name or not updateStudent.email or not updateStudent.date_of_birth or not updateStudent.gender or not updateStudent.phone or not updateStudent.address or not  updateStudent.parents_name or not  updateStudent.parents_phone_no:
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

@require_POST
def deleteStudent(request, id):
    deleteStudent = get_object_or_404(Customer, id=id)
    deleteStudent.delete()
    return redirect('student-index')


def addClient(request):
    if request.method == 'POST':
        try:
            Workspace_id = 1
            workspace = Workspace.objects.get(pk=Workspace_id)
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            image = None if not request.FILES.get('profile_image') else request.FILES.get('profile_image')
            email = request.POST.get('email')
           
            phone = request.POST.get('phone')
            address = request.POST.get('address') 
            document = None if not request.FILES.get('legal_document') else request.FILES.get('legal_document')
            company = request.POST.get('company')
            panno = request.POST.get('panno')

            if not first_name or not last_name or not email or not phone or not address or not company or not panno:
                messages.error(request, 'Please fill in all the required fields.')
                return redirect('add-client')
            
            new_client = Customer(
                first_name=first_name,
                last_name=last_name,
                profile_image=image,
                email=email,
                phone=phone,
                address=address,
                customer_type='client',
                workspace=workspace,
                legal_document=document,
                company=company,
                vat_pan_no=panno,
            )
            new_client.save()
            messages.success(request, 'Client added successfully.')
        except Exception as e:
           print(e)
           messages.error(request, 'An error occurred while saving the Clients.')
        return redirect('add-client')
    return render(request,'dashboard/pages/clients/add.html')


def editClient(request,id):
    editClients = get_object_or_404(Customer, customer_type='client', id=id)
    return render(request, 'dashboard/pages/clients/edit.html', {'editClient': editClients})

def updateClient(request, id):
    updateClient = get_object_or_404(Customer, customer_type='client', id=id) 

    
    if request.method == 'POST':
        updateClient.first_name = request.POST.get('first_name')
        updateClient.last_name = request.POST.get('last_name')
        if request.FILES.get('profile_image'):
            updateClient.profile_image = request.FILES.get('profile_image')
        updateClient.email = request.POST.get('email')
        
        updateClient.phone = request.POST.get('phone')
        updateClient.address = request.POST.get('address')
        updateClient.vat_pan_no = request.POST.get('panno')
        updateClient.company = request.POST.get('company')
        if request.FILES.get('legal_document'):
            updateClient.legal_document = request.FILES.get('legal_document')

        if not updateClient.first_name or not updateClient.last_name or not updateClient.email  or not updateClient.phone or not updateClient.address or not updateClient.vat_pan_no or not updateClient.company:
            messages.error(request, 'Please fill in all the required fields.')
            return redirect('update-client', id=id)

        try:
            updateClient.save()
            messages.success(request, 'Client updated successfully.')
            return redirect('client-index')
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
            return redirect('update-client', id=id)

    return render(request, 'dashboard/pages/clients/edit.html', {'updateClients': updateClient})


def deleteClient(request, id):
    deleteClient = Customer.objects.get(id=id)
    deleteClient.delete()
    return redirect('client-index')
 