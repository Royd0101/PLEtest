from django.shortcuts import render ,redirect
from .serializers import FileSerializer , DepartmentSerializer,FileLogSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.utils import timezone
from datetime import timedelta
from .models import File_Document ,Department , FileLog
from django.shortcuts import render, get_object_or_404
import requests
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages



#import from form
from .forms import create_file
from .forms import renew_form
from .forms import DepartmentForm

# Create your views here.

    
class Department_view(ModelViewSet):
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        user_company = self.request.user.company
        return Department.objects.filter(company=user_company)


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class File_Document_view(ModelViewSet):
    serializer_class = FileSerializer
    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
#get the expired file  
    @action(detail=False, methods=['get'])
    def expired(self, request):
        user_email = request.query_params.get('user_email') 
        queryset = self.get_queryset().filter(expiry_date__lt=timezone.now(), user__email=user_email)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
#get the valid file
    @action(detail=False, methods=['get'])
    def valid_file(self, request):
        user_email = request.query_params.get('user_email') 
        expiration_threshold = timezone.now() + timedelta(days=60)
        queryset = self.get_queryset().filter(
            expiry_date__gte=expiration_threshold,  user__email=user_email
        )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
#get the file to be renew
    @action(detail=False, methods=['get'])
    def to_be_renew(self, request):
        user_email = request.query_params.get('user_email') 
        two_months_before_expiry = timezone.now() + timedelta(days=60)
        queryset = self.get_queryset().filter(expiry_date__gte=timezone.now(), expiry_date__lte=two_months_before_expiry,user__email=user_email )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

#admin api
    #get the expired file

    @action(detail=False, methods=['get'])
    def admin_expired_list(self, request):
        queryset = self.get_queryset().filter(expiry_date__lt=timezone.now())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
#get the valid file
    @action(detail=False, methods=['get'])
    def admin_valid_list(self, request):
        expiration_threshold = timezone.now() + timedelta(days=60)
        queryset = self.get_queryset().filter(
            expiry_date__gte=expiration_threshold
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
#get the file to be renew
    @action(detail=False, methods=['get'])
    def admin_to_be_renew_list(self, request):
        two_months_before_expiry = timezone.now() + timedelta(days=60)
        queryset = self.get_queryset().filter(expiry_date__gte=timezone.now(), expiry_date__lte=two_months_before_expiry)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
class FileLog_view(ModelViewSet):
    serializer_class = FileLogSerializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



#user ---------------------------------------------------------------------------------------------
#get expired file list
@login_required
def get_expired_file_list(request):
    user_email = request.user.email
    response = requests.get('http://127.0.0.1:8000/api/file/expired/', params={'user_email': user_email})
    if response.status_code == 200 and response.text: 
        expired_file = response.json()
        
        return render(request, 'expired_file_list.html', {'expired_file': expired_file})
    else:
        error_message = f"Error fetching expired files. Status code: {response.status_code}"
        return render(request, 'error_page.html', {'error_message': error_message})


#get expired file list
@login_required
def get_valid_file_list(request):
    user_email = request.user.email
    response = requests.get('http://127.0.0.1:8000/api/file/valid_file/', params={'user_email': user_email})
    if response.status_code == 200:
        valid_file = response.json()
        return render(request, 'valid_file_list.html', {'valid_file': valid_file})
    else:
        return render(request, 'error_page.html')


#get expired file list
@login_required
def get_renew_file_list(request):
    user_email = request.user.email
    response = requests.get('http://127.0.0.1:8000/api/file/to_be_renew/', params={'user_email': user_email})
    if response.status_code == 200:
        renew_file = response.json()
        return render(request, 'to_be_renew_file_list.html', {'renew_file': renew_file})
    else:
        return render(request, 'error_page.html')

   
#function
#create new file 
@login_required
def create_new_file(request):
    if request.method == 'POST':
        form = create_file(request.user.company, request.POST, request.FILES)
        if form.is_valid():
            department_name = form.cleaned_data['department_name']
            department = Department.objects.get(department_name=department_name)

            file_document = File_Document(
                user=request.user,
                company=request.user.company,
                department_name=department,  
                document_type=form.cleaned_data['document_type'],
                agency=form.cleaned_data['agency'],
                upload_file=form.cleaned_data['upload_file'],
                renewal_date=form.cleaned_data['renewal_date'],
                expiry_date=form.cleaned_data['expiry_date']
            )
            file_document.save()

            log_entry = FileLog.objects.create(
                user=request.user,
                file=file_document,
                action='created'
            )

            messages.success(request, 'File created successfully!')
            return redirect('create_new_file_form')
        else:
            messages.error(request, 'Error creating file. Please check your inputs.')
    else:
        form = create_file(company=request.user.company)
    return render(request, 'create_new_file_form.html', {'form': form})


#renew the file 
@login_required
def renew_file(request, file_id):
    file = get_object_or_404(File_Document, id=file_id)
    if request.method == 'POST':
        form = renew_form(request.user.company, request.POST, request.FILES)
        if form.is_valid():
            department_name = form.cleaned_data['department_name']
            department = Department.objects.get(department_name=department_name)

            file.document_type = form.cleaned_data['document_type']
            file.agency = form.cleaned_data['agency']
            file.department_name = department  
            file.upload_file = form.cleaned_data['upload_file']
            file.renewal_date = form.cleaned_data['renewal_date']
            file.expiry_date = form.cleaned_data['expiry_date']
            file.save()

            # Create a log entry for the file renewal
            log_entry = FileLog.objects.create(
                user=request.user,
                file=file,
                action='renewed'
            )

            messages.success(request, 'File renewed successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Error renewing file. Please check your inputs.')
            print(f'Form Errors: {form.errors}')
    else:
        form = renew_form(request.user.company, initial={ 
            'document_type': file.document_type,
            'department_name': file.department_name.department_name,  
        })

    context = {'form': form, 'file': file}
    return render(request, 'renew_file_form.html', context)


#department list
@login_required
def department_list(request):
    department = Department.objects.all()
    context = {"department": department}
    return render(request, 'department_list.html', context)


#all pages

#display create new file pages
@login_required
def create_new_file_form(request):
    context = {'form': create_file(request.user.company)}
    return render(request, 'create_new_file_form.html', context)

#department form
@login_required
def department_page(request):
    form = DepartmentForm() 
    return render(request, 'admin_add_department.html' , {'form': form})

@login_required
def create_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department_page')  
    else:
        form = DepartmentForm()

    return render(request, 'admin_add_department.html', {'form': form})

#display logs
@login_required
def users_logs(request):
    logs = FileLog.objects.all().order_by('-timestamp')
    return render(request, 'file_logs.html', {'logs': logs})


#display renew file pages
@login_required
def renew_file_form(request, file_id):
    file = get_object_or_404(File_Document, id=file_id)
    form = renew_form(company=request.user.company, initial={
        'document_type': file.document_type,
        'department': file.department_name,
        'agency': file.agency,
    }) 
    context = {'form': form, 'file': file}
    return render(request, 'renew_file_form.html', context)

#admin dashboard page
@login_required
def display_admin_expired(request):
    return render(request, 'admin_expired_file.html')
@login_required
def display_admin_valid(request):
    return render(request, 'admin_valid_file.html')
@login_required
def display_admin_to_be_renew(request):
    return render(request, 'admin_renew_file.html')

@login_required
def display_file_page(request, file_id):
    file_profile = File_Document.objects.get(pk=file_id)  
    return render(request, 'file_profile.html', {'file_profile': file_profile})

#dashboard ge total
@login_required
def dashboard_total_expired(request):
    user_email = request.user.email
    response = requests.get('http://127.0.0.1:8000/api/file/expired/', params={'user_email': user_email})
    if response.status_code == 200 and response.text: 
        expired_file = response.json()
        total_expired_document = len(expired_file)
    else:
        total_expired_document = 0
    return render(request, 'dashboard.html', {'total_expired_document': total_expired_document})

@login_required
def dashboard_total_valid(request):
    user_email = request.user.email
    response = requests.get('http://127.0.0.1:8000/api/file/valid_file/', params={'user_email': user_email})
    if response.status_code == 200 and response.text: 
        expired_file = response.json()
        total_valid_document = len(expired_file)
    else:
        total_valid_document = 0
    return render(request, 'dashboard.html', {'total_valid_document': total_valid_document})

@login_required
def dashboard_total_renew(request):
    user_email = request.user.email
    response = requests.get('http://127.0.0.1:8000/api/file/to_be_renew/', params={'user_email': user_email})
    if response.status_code == 200 and response.text: 
        expired_file = response.json()
        total_to_be_renew_document = len(expired_file)
    else:
        total_to_be_renew_document = 0
    return render(request, 'dashboard.html', {'total_to_be_renew_document': total_to_be_renew_document})