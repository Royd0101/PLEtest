from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer, CompanySerializer
from django.contrib import messages
import requests
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from .models import User, Company
from rest_framework import status
from django.contrib.auth.decorators import login_required
#import from form
from .forms import create_user_form
from .forms import update_user_form
from .forms import company_form ,update_company_form
from django.http import HttpResponse
from collections import Counter
from datetime import datetime
from rest_framework.decorators import api_view
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test


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
                messages.warning(request, 'Passwords do not match. Please try again.')
                form.add_error('confirm_password', 'Passwords do not match.')
                return render(request, 'create_user_form.html', {'form': form})

            # Check if the email is already in use
            if User.objects.filter(email=email).exists():
                messages.warning(request, 'This email is already taken. Please choose a different one.')
                form.cleaned_data['password'] = ''
                form.cleaned_data['confirm_password'] = ''
                return render(request, 'create_user_form.html', {'form': form})

            user = User.objects.create_user(email=email, password=password, company=company, first_name=first_name, last_name=last_name)

            messages.success(request, 'User Created successfully!')
            return redirect('create_user_page') 
        else:
            messages.warning(request, 'Invalid input. Please check your inputs.')
            form.cleaned_data['password'] = ''
            form.cleaned_data['confirm_password'] = ''
    else:
        form = create_user_form()
    return render(request, 'create_user_form.html', {'form': form})



#update user data -----------------------------------------------------------------------------
@user_passes_test(lambda u: u.is_superuser)  # Only allow superusers
@login_required
def update_users(request, user_id):
    user = get_object_or_404(User, id=user_id,)
    if request.method == 'POST':
        form = update_user_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('user_list')
        else:
            messages.warning(request, 'Please correct the errors below.')
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
    return render(request, 'admin_user_list.html', context)


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
            messages.warning(request, 'Email or Password not found.')
    return render(request, 'login.html')

    
#logout user
@login_required
def logout_user(request):
    logout(request)
    return redirect('redirect_to_login')

#dashboard page --------------------------------------------------------------------------------
@login_required
def dashboard(request):

    admin_response1 = requests.get('http://127.0.0.1:8000/api/file/valid_documents/')
    admin_response2 = requests.get('http://127.0.0.1:8000/api/file/renewal_documents/')
    admin_response3 = requests.get('http://127.0.0.1:8000/api/file/expired_documents/')
    admin_response4 = requests.get('http://127.0.0.1:8000/api/receipts/')

    user_email = request.user.email  
    response1 = requests.get('http://127.0.0.1:8000/api/file/valid_file/', params={'user_email': user_email})
    response2 = requests.get('http://127.0.0.1:8000/api/file/expired/', params={'user_email': user_email})
    response3 = requests.get('http://127.0.0.1:8000/api/file/to_be_renew/', params={'user_email': user_email})
    response4 = requests.get('http://127.0.0.1:8000/api/receipts/receipt', params={'user_email': user_email})

    user_response1 = requests.get('http://127.0.0.1:8000/api/file/person_valid/', params={'user_email': user_email})
    user_response2 = requests.get('http://127.0.0.1:8000/api/file/person_renew/', params={'user_email': user_email})
    user_response3 = requests.get('http://127.0.0.1:8000/api/file/person_expired/', params={'user_email': user_email})
    user_response4 = requests.get('http://127.0.0.1:8000/api/receipts/user_receipt/', params={'user_email': user_email})

    num_valid_files = num_expired_files = num_renew_files = num_penalty_files = 0
    admin_num_valid_files = admin_num_expired_files = admin_num_renew_files  = admin_num_penalty_files= 0

#admin display person document
    admin_person_response1 = requests.get('http://127.0.0.1:8000/api/file/person_valid_documents/')
    admin_person_response2 = requests.get('http://127.0.0.1:8000/api/file/person_renew_documents/')
    admin_person_response3 = requests.get('http://127.0.0.1:8000/api/file/person_expired_documents/')
    admin_person_response4 = requests.get('http://127.0.0.1:8000/api/receipts/person_receipt/')

    

    person_valid_files = person_expired_files = person_renew_files  = person_fined_files = 0

    user_person_valid_files = user_person_expired_files = user_person_renew_files  = user_person_fined_files = 0

    if admin_person_response1.status_code == 200:
        person_total_valid = admin_person_response1.json()
        person_valid_files = len(person_total_valid)

        
    if admin_person_response2.status_code == 200:
        person_total_renew = admin_person_response2.json()
        person_renew_files = len(person_total_renew)


    if admin_person_response3.status_code == 200:
        person_total_expired = admin_person_response3.json()
        person_expired_files = len(person_total_expired)

    if admin_person_response4.status_code == 200:
        person_total_fined = admin_person_response4.json()
        person_fined_files = len(person_total_fined)



    #user side person documents
        #valid
    if user_response1.status_code == 200:
        user_person_total_valid = user_response1.json()
        user_person_valid_files = len(user_person_total_valid)

        #renew
    if user_response2.status_code == 200:
        user_person_total_renew = user_response2.json()
        user_person_renew_files = len(user_person_total_renew)

        #expired
    if user_response3.status_code == 200:
        user_person_total_expired = user_response3.json()
        user_person_expired_files = len(user_person_total_expired)

    if user_response4.status_code == 200:
        user_person_total_fined = user_response4.json()
        user_person_fined_files = len(user_person_total_fined)


#admin display business data

    if response1.status_code == 200:
        total_valid = response1.json()
        num_valid_files = len(total_valid)
        agencies1 = [item.get('agency') for item in total_valid]
        agency_counts1 = dict(Counter(agencies1))
        
    if response2.status_code == 200:
        total_expired = response2.json()
        num_expired_files = len(total_expired)
        agencies2 = [item.get('agency') for item in total_expired]
        agency_counts2 = dict(Counter(agencies2))

    if response3.status_code == 200:
        total_renew = response3.json()
        num_renew_files = len(total_renew)
        agencies3 = [item.get('agency') for item in total_renew]
        agency_counts3 = dict(Counter(agencies3))
    
    if response4.status_code == 200:
        penalty_document = response4.json()
        num_penalty_files = len(penalty_document)
        agencies4 = [item.get('agency') for item in penalty_document]
        agency_counts4 = dict(Counter(agencies4))

#admin
    if admin_response1.status_code == 200:
        admin_total_valid = admin_response1.json()
        admin_num_valid_files = len(admin_total_valid)

        admin_agency_counts_by_company = {}

        for item in admin_total_valid:
            company_name = item.get('company_name')  
            agency = item.get('agency')
            if company_name not in admin_agency_counts_by_company:
                admin_agency_counts_by_company[company_name] = {}

            if agency not in admin_agency_counts_by_company[company_name]:
                admin_agency_counts_by_company[company_name][agency] = 1
            else:
                admin_agency_counts_by_company[company_name][agency] += 1
        
    if admin_response2.status_code == 200:
        admin_total_renew = admin_response2.json()
        admin_num_renew_files = len(admin_total_renew)
        
        admin_agency_counts_by_company1 = {}

        for item in admin_total_renew:
            company_name = item.get('company_name')  
            agency = item.get('agency')
            if company_name not in admin_agency_counts_by_company1:
                admin_agency_counts_by_company1[company_name] = {}

            if agency not in admin_agency_counts_by_company1[company_name]:
                admin_agency_counts_by_company1[company_name][agency] = 1
            else:
                admin_agency_counts_by_company1[company_name][agency] += 1

    if admin_response3.status_code == 200:
        admin_total_expired = admin_response3.json()
        admin_num_expired_files = len(admin_total_expired)
        admin_agency_counts_by_company2 = {}

        for item in admin_total_expired:
            company_name = item.get('company_name')  
            agency = item.get('agency')
            if company_name not in admin_agency_counts_by_company2:
                admin_agency_counts_by_company2[company_name] = {}

            if agency not in admin_agency_counts_by_company2[company_name]:
                admin_agency_counts_by_company2[company_name][agency] = 1
            else:
                admin_agency_counts_by_company2[company_name][agency] += 1
    
    if admin_response4.status_code == 200:
        admin_total_penalty = admin_response4.json()
        admin_num_penalty_files = len(admin_total_penalty)
        admin_agency_counts_by_company3 = {}

        for item in admin_total_penalty:
            company_name = item.get('company_name')  
            agency = item.get('agency')
            if company_name not in admin_agency_counts_by_company3:
                admin_agency_counts_by_company3[company_name] = {}

            if agency not in admin_agency_counts_by_company3[company_name]:
                admin_agency_counts_by_company3[company_name][agency] = 1
            else:
                admin_agency_counts_by_company3[company_name][agency] += 1

    context = {
            'num_valid': num_valid_files,
            'num_expired': num_expired_files,
            'num_renew': num_renew_files,
            'num_penalty': num_penalty_files,
            'a_c1': agency_counts1,
            'a_c2': agency_counts2,
            'a_c3': agency_counts3,
            'a_c4': agency_counts4,
            'admin_c1': admin_num_valid_files,
            'admin_c2': admin_num_renew_files,
            'admin_c3': admin_num_expired_files,
            'admin_c4': admin_num_penalty_files,
            'admin_a1': admin_agency_counts_by_company,
            'admin_a2': admin_agency_counts_by_company1,
            'admin_a3': admin_agency_counts_by_company2,
            'admin_a4': admin_agency_counts_by_company3,
            'person_valid': person_valid_files,
            'person_renew': person_renew_files,
            'person_expired': person_expired_files,
            'user_p_expired': user_person_expired_files,
            'user_p_renew': user_person_renew_files,
            'user_p_valid': user_person_valid_files,
            'person_fined': person_fined_files,
            'user_pe_fined': user_person_fined_files,
        }

    return render(request, 'dashboard.html',context)


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
            messages.warning(request, 'A company with this name already exists.')
    else:
        form = company_form()

    return render(request, 'admin_add_company.html', {'form': form})

@login_required
def update_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    if request.method == 'POST':
        form = update_company_form(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('company_list')
    else:
        form = update_company_form(initial={'company_name': company.company_name})

    context = {'company': company, 'form': form}
    return render(request, 'update_company.html', context)

@login_required
def delete_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    if request.method == 'POST':
        company.delete()
        messages.success(request, f'Company "{company.company_name}" has been deleted.')
        return redirect('company_list')

    context = {'company': company}
    return render(request, 'company_list.html', context)

  
@api_view(['GET'])
def department_total_fine(request):
    user_email = request.user.email
    api_url = 'http://127.0.0.1:8000/api/receipts/receipt'
    try:
        response = requests.get(api_url, params={'user_email': user_email})
        response.raise_for_status()

        sample = response.json()
        department_totals = {}

        for entry in sample:
            department = entry.get('department_name', 'Unknown Department')
            fined_value = float(entry.get('fined', 0))
            
            # Use the timestamp as the basis for fines
            timestamp_str = entry.get('timestamp', '')
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%fZ') if timestamp_str else timezone.now()

            # Extract year from timestamp
            document_expiry_year = timestamp.year

            # Include the year in the key
            key = f"{department} - {document_expiry_year}"
            total_fines = department_totals.get(key, 0) + fined_value
            department_totals[key] = total_fines
            

        # Sort the keys based on the extracted year
        sorted_department_totals = dict(sorted(department_totals.items(), key=lambda x: x[1]))

        return Response(sorted_department_totals)
    except requests.RequestException as e:
        return Response({"error": f"Error fetching data from the API: {str(e)}"}, status=500)



