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
from users.models import Company
from .email_utils import send_notification_email
from django.shortcuts import HttpResponse
from .tasks import check_document_expiry
#import from form
from .forms import create_file
from .forms import renew_form
from .forms import DepartmentForm,update_department_form
from django.db.models import Count
from django.conf import settings
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
        agency_counts = queryset.values('agency').annotate(count=Count('agency'))
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
        agency_counts = queryset.values('agency').annotate(count=Count('agency'))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
#get the file to be renew
    @action(detail=False, methods=['get'])
    def to_be_renew(self, request):
        user_email = request.query_params.get('user_email') 
        two_months_before_expiry = timezone.now() + timedelta(days=60)
        queryset = self.get_queryset().filter(expiry_date__gte=timezone.now(), expiry_date__lte=two_months_before_expiry,user__email=user_email )
        agency_counts = queryset.values('agency').annotate(count=Count('agency'))
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
        agency_counts = queryset.values('company__company_name', 'agency').annotate(count=Count('agency'))
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
    
    @action(detail=False, methods=['get'])
    def user_list_log(self, request, *args, **kwargs):
        user_email = request.query_params.get('user_email') 
        queryset = self.get_queryset().filter(user__email=user_email)
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
def get_renew_file_list(request):
    user_email = request.user.email
    response = requests.get('http://127.0.0.1:8000/api/file/to_be_renew/', params={'user_email': user_email})
    if response.status_code == 200:
        renew_file = response.json()
        return render(request, 'to_be_renew_file_list.html', {'renew_file': renew_file})
    else:
        return render(request, 'error_page.html')
        
    
#admin list
@login_required
def admin_expired_file_list(request):
    response = requests.get('http://127.0.0.1:8000/api/file/expired_documents/')
    if response.status_code == 200 and response.text: 
        admin_expired1 = response.json()
        return render(request, 'admin_expired_file.html', {'admin_expired1': admin_expired1})
    else:
        error_message = f"Error fetching expired files. Status code: {response.status_code}"
        return render(request, 'error_page.html', {'error_message': error_message})
    
@login_required
def admin_valid_file_list(request):
    file_documents_with_receipts = File_Document.objects.prefetch_related('receipt_set').all()
    response = requests.get('http://127.0.0.1:8000/api/receipts/')
    
    if response.status_code == 200 and response.text:
        admin_total_fined = response.json()
        admin_total_fine = sum(float(item['fined']) if item['fined'] else 0 for item in admin_total_fined)
    context = {
        'file_documents_with_receipts': file_documents_with_receipts,
        'admin_total_fine':admin_total_fine,
    }
    return render(request, 'admin_valid_file.html', context)
    
@login_required
def admin_renew_file_list(request):
    response = requests.get('http://127.0.0.1:8000/api/file/renewal_documents/')
    if response.status_code == 200 and response.text: 
        admin_renew1 = response.json()
        return render(request, 'admin_renew_file.html', {'admin_renew1': admin_renew1})
    else:
        error_message = f"Error fetching expired files. Status code: {response.status_code}"
        return render(request, 'error_page.html', {'error_message': error_message})


@login_required
def user_logs(request):
    user = request.user.email
    response = requests.get('http://127.0.0.1:8000/api/file/user_log/', params={'user_email': user})
    if response.status_code == 200:
        user_log = response.json()

        for log_entry in user_log:
            timestamp_utc = timezone.datetime.strptime(log_entry['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ")
            timestamp_manila = timestamp_utc + timezone.timedelta(hours=0)  
            log_entry['timestamp'] = timestamp_manila.strftime("%Y-%m-%d %I:%M %p")  

            for log_entry in user_log:
                log_entry['current_file_url'] = f"{settings.MEDIA_URL}{log_entry.get('current_file_name', '')}"
                log_entry['previous_file_url'] = f"{settings.MEDIA_URL}{log_entry.get('previous_file_name', '')}"


        user_log.sort(key=lambda x: timezone.datetime.strptime(x['timestamp'], "%Y-%m-%d %I:%M %p"), reverse=True)

        return render(request, 'file_logs.html', {'user_log': user_log})
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
            department = Department.objects.filter(
                department_name=department_name,
                company=request.user.company
            ).first()

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
            print(department_name)
            file_document.save()

            log_entry = FileLog.objects.create(
                user=request.user,
                file=file_document,
                expiry_date= file_document.expiry_date,
                action='created'
            )

            messages.success(request, 'File created successfully!')
            return redirect('create_new_file_form')
        else:
            messages.warning(request, 'Error creating file. Please check your inputs.')
    else:
        form = create_file(company=request.user.company)
    return render(request, 'create_new_file_form.html', {'form': form})


#renew the file 
@login_required
def renew_file(request, file_id):
    file = get_object_or_404(File_Document, id=file_id)
    previous_file_path = file.upload_file.path  # Save the path of the old file

    if request.method == 'POST':
        form = renew_form(request.user.company, request.POST, request.FILES)
        if form.is_valid():
            department_name = form.cleaned_data['department_name']
            department = Department.objects.filter(
                department_name=department_name,
                company=request.user.company
            ).first()
            file.department_name = department 
            file.document_type = form.cleaned_data['document_type']
            file.agency = form.cleaned_data['agency']
            file.upload_file = form.cleaned_data['upload_file']
            file.renewal_date = form.cleaned_data['renewal_date']
            file.expiry_date = form.cleaned_data['expiry_date']
            file.save()

            # Create a log entry for the file renewal
            log_entry = FileLog.objects.create(
                user=request.user,
                file=file,
                previous_file=previous_file_path,  # Assign file path directly
                action='renewed'
            )

            messages.success(request, 'File renewed successfully!')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Error renewing file. Please check your inputs.')
            print(f'Form Errors: {form.errors}')
    else:
        form = renew_form(request.user.company, initial={ 
            'document_type': file.document_type,
            'department_name': file.department_name.department_name,
            'agency': file.agency, 
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
            messages.success(request, 'Department created successfully.')
            return redirect('department_list')  
        else:
            messages.warning(request, 'A department with this name already exists in this company.')
    else:
        form = DepartmentForm()
    return render(request, 'admin_add_department.html', {'form': form})

#display logs
@login_required
def admin_logs(request):
    response = requests.get('http://127.0.0.1:8000/api/file/logs/')
    if response.status_code == 200:
        admin_logs = response.json()

        # Convert timestamp to Philippines time and update the logs
        for log_entry in admin_logs:
            timestamp_utc = timezone.datetime.strptime(log_entry['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ")
            timestamp_manila = timestamp_utc + timezone.timedelta(hours=0) 
            log_entry['timestamp'] = timestamp_manila.strftime("%Y-%m-%d %I:%M %p") 

            for log_entry in admin_logs:
                log_entry['current_file_url'] = f"{settings.MEDIA_URL}{log_entry.get('current_file_name', '')}" 

        # Sort logs based on the converted timestamp
        admin_logs = sorted(admin_logs, key=lambda x: timezone.datetime.strptime(x['timestamp'], "%Y-%m-%d %I:%M %p"), reverse=True)

        return render(request, 'file_logs.html', {'admin_logs': admin_logs})
    else:
        return render(request, 'error_page.html')
    
@login_required
def admin_view(request, log_id):
    log_api_url = f'http://127.0.0.1:8000/api/file/logs/{log_id}/'
    response = requests.get(log_api_url)

    if response.status_code == 200:
        log_view = response.json()
        log_view['current_file_url'] = f"{settings.MEDIA_URL}{log_view.get('current_file_name', '')}"
        return render(request, 'view_file.html', {'log_view': log_view})
    else:
        return render(request, 'error_page.html')

   

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



@login_required
def display_file_page(request, file_id):
    file_profile = File_Document.objects.get(pk=file_id)  
    return render(request, 'file_profile.html', {'file_profile': file_profile})


@login_required
def update_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    
    if request.method == 'POST':
        form = update_department_form(request.POST)
        if form.is_valid():
            company = form.cleaned_data['company']
            company_name = Company.objects.get(company_name=company)
           
            department.company = company_name
            department.department_name = form.cleaned_data['department_name']
            department.save()
            return redirect('department_list')
    else:
        initial_data = {
            'company': department.company, 
            'department_name': department.department_name,
        }
        form = update_department_form(initial=initial_data) 

    context = {'form': form, 'department': department}
    return render(request, 'update_department.html', context)

#delete department
@login_required
def delete_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)

    if request.method == 'POST':
        department.delete()
        messages.success(request, f'Department "{department.department_name}" has been deleted.')
        return redirect('department_list')

    context = {'department': department}
    return render(request, 'department_list.html', context)


#sending email
@login_required
def automatic_send_mail(request):
    result = check_document_expiry.delay()
    return HttpResponse("Task scheduled.")


def file_documents_with_receipts(request):
    current_user = request.user
    response = requests.get('http://127.0.0.1:8000/api/receipts/receipt', params={'user_email': current_user})
    
    if response.status_code == 200 and response.text:
        total_fined = response.json()
        total_fine = sum(float(item['fined']) if item['fined'] else 0 for item in total_fined)
    
    file_documents_with_receipts = File_Document.objects.filter(user=current_user).prefetch_related('receipt_set').all()
    
    context = {
        'file_documents_with_receipts': file_documents_with_receipts,
        'total_fine': total_fine,  # Corrected placement of the total_fine key
    }
    
    return render(request, 'valid_file_list.html', context)




@login_required
def sample(request):
    user_email = request.user.email
    response = requests.get('http://127.0.0.1:8000/api/receipts/receipt/', params={'user_email': user_email})
    
    if response.status_code == 200 and response.text:
        sample = response.json()
        unique_departments = set(entry['department_name'] for entry in sample)
        department_files = {}

        unique_departments = set()
        unique_sample = [entry for entry in sample if entry['department_name'] not in unique_departments and not unique_departments.add(entry['department_name'])]

        for department in unique_departments:
            department_files[department] = [entry for entry in sample if entry['department_name'] == department]

        return render(request, 'sample.html', {'sample': unique_sample, 'department_files': department_files})
    else:
        error_message = f"Error fetching expired files. Status code: {response.status_code}"
        return render(request, 'error_page.html', {'error_message': error_message})
