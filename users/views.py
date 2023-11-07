from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer, CompanySerializer
from django.contrib import messages
import requests
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from .models import User, Company
from rest_framework import status
from django.contrib.auth.decorators import login_required
#import from form
from .forms import create_user_form
from .forms import update_user_form
from .forms import company_form 
from django.http import HttpResponse


# Create your views here.
class Company_views(ModelViewSet):
    serializer_class = CompanySerializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.order_by('id')
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class Users(ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.order_by('id')
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

#all function

#create user function -----------------------------------------------------------------------------
@login_required
def create_user(request):
    if request.method == 'POST':
        form = create_user_form(request.POST) 
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            company = form.cleaned_data['company']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                messages.error(request, 'Passwords do not match. Please try again.')
                form.cleaned_data['password'] = ''
                form.cleaned_data['confirm_password'] = ''
                return render(request, 'create_user_form.html', {'form': form})

            # Check if the email is already in use
            if User.objects.filter(email=email).exists():
                messages.error(request, 'This email is already taken. Please choose a different one.')
                form.cleaned_data['password'] = ''
                form.cleaned_data['confirm_password'] = ''
                return render(request, 'create_user_form.html', {'form': form})

            user = User.objects.create_user(email=email, password=password, company=company, first_name=first_name, last_name=last_name)

            messages.success(request, 'User Created successfully!')
            return redirect('create_user_page') 
        else:
            messages.warning(request, 'Invalid form. Please check your inputs.')
            form.cleaned_data['password'] = ''
            form.cleaned_data['confirm_password'] = ''
    else:
        form = create_user_form()
    return render(request, 'create_user_form.html', {'form': form})



#display update user page -----------------------------------------------------------------------
@login_required
def user_update(request, user_id):
    user = get_object_or_404(User, id=user_id)

    initial = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'company': user.company,
    }

    form = update_user_form(initial=initial)
    context = {'form': form}
    return render(request, 'update_user.html', context)

#update user data -----------------------------------------------------------------------------
@login_required
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = update_user_form(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            if form.cleaned_data['email'] != user.email:
                user.email = form.cleaned_data['email']
            company = form.cleaned_data['company']
            company_name = Company.objects.get(company_name=company)
            user.company = company_name
            
            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])
            
            user.save()
            messages.success(request, 'User updated successfully.')
            return redirect('user_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = update_user_form(initial={ 
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'company': user.company,
        })
    
    context = {'user': user, 'form': form}
    return render(request, 'update_user.html', context)



#delete department
@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.delete()
        messages.success(request, f'user has been deleted.')
        return redirect('user_list')

    context = {'user': user}
    return render(request, 'user_list.html', context)


#all pages--------------------------------------------------------------------------------------------
#root
def redirect_to_login(request):
    return redirect('login_page')

#render login page
def login_page(request):
    return render(request, 'login.html')

#login user
def login_user(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'User login Successfully.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Email or Password not found.')
    return render(request, 'login.html')

    
#logout user
@login_required
def logout_user(request):
    logout(request)
    return redirect('redirect_to_login')

@login_required
def chart(request):
    user_email = request.user.email
    response1 = requests.get('http://127.0.0.1:8000/api/file/valid_file/', params={'user_email': user_email})
    response2 = requests.get('http://127.0.0.1:8000/api/file/expired/', params={'user_email': user_email})
    response3 = requests.get('http://127.0.0.1:8000/api/file/to_be_renew/', params={'user_email': user_email})

    num_valid_files = num_expired_files = num_renew_files = 0

    if response1.status_code == 200:
        total_valid = response1.json()
        num_valid_files = len(total_valid)
        
    if response2.status_code == 200:
        total_expired = response2.json()
        num_expired_files = len(total_expired)

    if response3.status_code == 200:
        total_renew = response3.json()
        num_renew_files = len(total_renew)
    
    total_files = num_valid_files + num_expired_files + num_renew_files

    return render(request, 'chart.html', {'num_valid_files': num_valid_files, 'num_expired_files': num_expired_files, 'num_renew_files': num_renew_files, 'total_files':total_files})


#dashboard page --------------------------------------------------------------------------------
@login_required
def dashboard(request):
    user_email = request.user.email
    response1 = requests.get('http://127.0.0.1:8000/api/file/valid_file/', params={'user_email': user_email})
    response2 = requests.get('http://127.0.0.1:8000/api/file/expired/', params={'user_email': user_email})
    response3 = requests.get('http://127.0.0.1:8000/api/file/to_be_renew/', params={'user_email': user_email})

    num_valid_files = num_expired_files = num_renew_files = 0

    if response1.status_code == 200:
        total_valid = response1.json()
        num_valid_files = len(total_valid)
        
    if response2.status_code == 200:
        total_expired = response2.json()
        num_expired_files = len(total_expired)

    if response3.status_code == 200:
        total_renew = response3.json()
        num_renew_files = len(total_renew)
    
    total_files = num_valid_files + num_expired_files + num_renew_files

    return render(request, 'dashboard.html', {'num_valid_files': num_valid_files, 'num_expired_files': num_expired_files, 'num_renew_files': num_renew_files, 'total_files':total_files})


#create user page -----------------------------------------------------------------------------
@login_required
def create_user_page(request):
    form = create_user_form() 
    return render(request, 'create_user_form.html' , {'form': form})

#create company page
@login_required
def company_page(request):
    form = company_form() 
    return render(request, 'admin_add_company.html' , {'form': form})

#display user list page -----------------------------------------------------------------------
@login_required
def user_list(request):
    if request.user.is_staff:
        users = User.objects.filter(is_staff=False).order_by('first_name')
        context = {"users": users}
        return render(request, 'user_list.html', context)
    else:
        return HttpResponse("You do not have permission to access this page.")

#get company list
@login_required     
def company_list(request):
    response = requests.get('http://127.0.0.1:8000/api/users/company/')
    if response.status_code == 200 and response.text: 
        list_company = response.json()
        return render(request, 'company_list.html', {'list_company': list_company})
    else:
        error_message = f"Error fetching expired files. Status code: {response.status_code}"
        return render(request, 'error_page.html', {'error_message': error_message})


@login_required
def create_company(request):
    if request.method == 'POST':
        form = company_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company created successfully.')  
            return redirect('company_page')
        else:
            messages.error(request, 'A company with this name already exists.')
    else:
        form = company_form()

    return render(request, 'admin_add_company.html', {'form': form})

@login_required
def delete_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    if request.method == 'POST':
        company.delete()
        messages.success(request, f'Company "{company.company_name}" has been deleted.')
        return redirect('company_list')

    context = {'company': company}
    return render(request, 'company_list.html', context)