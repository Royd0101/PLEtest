from rest_framework import serializers
from .models import Receipt


class ReceiptSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='file.user.email', read_only=True)
    first_name = serializers.EmailField(source='file.user.first_name', read_only=True)
    last_name = serializers.EmailField(source='file.user.last_name', read_only=True)
    department_name = serializers.CharField(source='file.department_name', read_only=True)
    company_name = serializers.EmailField(source='file.company', read_only=True)
    document_type = serializers.CharField(source='file.document_type', read_only=True)
    expiry_date = serializers.EmailField(source='file.expiry_date', read_only=True)
    renewal_date = serializers.CharField(source='file.renewal_date', read_only=True)
    document = serializers.FileField(source='file.upload_file', read_only=True)
    agency = serializers.EmailField(source='file.agency', read_only=True)
    class Meta:
        model =  Receipt
        fields = (
            'id',
            'user_email',
            'fined',
            'file',
            'department_name',
            'company_name',
            'expiry_date',
            'renewal_date',
            'document_type',
            'document',
            'agency',
            'receipt',
            'first_name',
            'last_name',
        )