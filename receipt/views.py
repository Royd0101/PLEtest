from django.shortcuts import render, redirect
from rest_framework.viewsets import ModelViewSet
from .serializers import ReceiptSerializer
from django.contrib import messages
from .forms import receipt_form
from .models import Receipt
from files.models import File_Document
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
import requests
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
def receipt_valid_documents(request):
    user = request.user.email
    response = requests.get('http://127.0.0.1:8000/api/receipts/receipt', params={'user_email': user})
    if response.status_code == 200 and response.text: 
        valid_receipts = response.json()
        user_total_fine = sum(float(item['fined']) if item['fined'] else 0 for item in valid_receipts)
        return render(request, 'fined_document.html', {'valid_receipts': valid_receipts ,'user_total_fine':user_total_fine})
    else:
        error_message = f"Error fetching expired files. Status code: {response.status_code}"
        return render(request, 'error_page.html', {'error_message': error_message})
    

@login_required
def admin_receipt_documents(request):
    user = request.user.email
    response = requests.get('http://127.0.0.1:8000/api/receipts/', params={'user_email': user})
    if response.status_code == 200 and response.text: 
        fine_document = response.json()

        total_fine = sum(float(item['fined']) if item['fined'] else 0 for item in fine_document)
        return render(request, 'admin_fine_document.html', {'fine_document': fine_document, 'total_fine': total_fine})
    else:
        error_message = f"Error fetching expired files. Status code: {response.status_code}"
        return render(request, 'error_page.html', {'error_message': error_message})