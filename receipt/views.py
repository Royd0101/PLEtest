from django.shortcuts import render, redirect
from rest_framework.viewsets import ModelViewSet
from .serializers import ReceiptSerializer, Person_ReceiptSerializer
from django.contrib import messages
from .forms import receipt_form ,person_receipt_form
from .models import Receipt ,Person_Document
from files.models import File_Document
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
import requests
from rest_framework import status
from datetime import datetime
# Create your views here.

class Receipt_view(ModelViewSet):
    serializer_class = ReceiptSerializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
    
    @action(detail=False, methods=['get'])
    def receipt(self, request, *args, **kwargs):
        user_email = request.query_params.get('user_email')
        queryset = self.get_queryset().filter(file__user__email=user_email)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class Person_Receipt_view(ModelViewSet):
    serializer_class = Person_ReceiptSerializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
    
@login_required
def create_receipt(request, file_id):
    file = get_object_or_404(File_Document, id=file_id)
    if request.method == 'POST':
        form = receipt_form(request.POST, request.FILES)

        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.file = file
            receipt.save()

            messages.success(request, 'Uploaded successfully!')
            return redirect('renew_file', file_id=file.id)
        else:
            messages.warning(request, 'Error uploading file. Please check your inputs.')
            print(f'Form Errors: {form.errors}')
    else:
        form = receipt_form(initial={'file': file})

    context = {'form': form, 'file': file}
    return render(request, 'receipt.html', context)


@login_required
def create_person_receipt(request, document_id):
    file = get_object_or_404(Person_Document, id=document_id)
    if request.method == 'POST':
        form = person_receipt_form(request.POST, request.FILES)

        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.file = file
            receipt.save()

            messages.success(request, 'Uploaded successfully!')
            return redirect('renew_person_documents', document_id=file.id)
        else:
            messages.warning(request, 'Error uploading file. Please check your inputs.')
            print(f'Form Errors: {form.errors}')
    else:
        form = person_receipt_form(initial={'file': file})

    context = {'form': form, 'file': file}
    return render(request, 'person_receipt.html', context)

@login_required
def receipt_valid_documents(request):
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

        return render(request, 'fined_document.html', {'sample': unique_sample,'total_doc':sample ,'department_files': department_files})
    else:
        error_message = f"Error fetching expired files. Status code: {response.status_code}"
        return render(request, 'error_page.html', {'error_message': error_message})
    

@login_required
def admin_receipt_documents(request):
    response = requests.get('http://127.0.0.1:8000/api/receipts/')
    if response.status_code == 200 and response.text:
        fine_document = response.json()
        unique_years = set(entry['expiry_date'][:4] for entry in fine_document)

        filter_year = request.GET.get('filter_year', 'all')
        if filter_year != 'all':
            fine_document = [entry for entry in fine_document if entry['expiry_date'][:4] == filter_year]

        unique_companies = set(entry['company_name'] for entry in fine_document)
        company_files = {}

        # Filter unique samples based on company_name
        unique_sample = [entry for entry in fine_document if entry['company_name'] not in unique_companies and not unique_companies.add(entry['company_name'])]

        # Create a dictionary of company files
        for company in unique_companies:
            company_files[company] = [entry for entry in fine_document if entry['company_name'] == company]

        return render(request, 'admin_fine_document.html', {'sample': unique_sample, 'total_doc': fine_document, 'company_files': company_files, 'unique_years': unique_years, 'selected_year': filter_year})
    else:
        error_message = f"Error fetching expired files. Status code: {response.status_code}"
        return render(request, 'error_page.html', {'error_message': error_message})


@login_required
def admin_person_receipt_documents(request):
    api_response = requests.get('http://127.0.0.1:8000/api/receipts/person_receipt/')
    if api_response.status_code == 200 and api_response.text:
        fined_documents = api_response.json()
        unique_years = set(entry['expiry_date'][:4] for entry in fined_documents)

        filter_year = request.GET.get('filter_year', 'all')

        if filter_year != 'all':
            fined_documents = [entry for entry in fined_documents if entry['expiry_date'][:4] == filter_year]

        unique_companies = set(entry['company_name'] for entry in fined_documents)
        company_files = {}

        unique_samples = [entry for entry in fined_documents if entry['company_name'] not in unique_companies and not unique_companies.add(entry['company_name'])]

        for company in unique_companies:
            company_files[company] = [entry for entry in fined_documents if entry['company_name'] == company]

        return render(request, 'person_fined_documents.html', {'unique_samples': unique_samples, 'total_documents': fined_documents, 'company_files': company_files, 'unique_years': unique_years, 'selected_year': filter_year})
    else:
        error_message = f"Error fetching expired files. Status code: {api_response.status_code}"
        return render(request, 'error_page.html', {'error_message': error_message})
    


    
        