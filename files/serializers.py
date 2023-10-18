from rest_framework import serializers
from files.models import File_Document, Department,FileLog

class FileSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_firstname = serializers.EmailField(source='user.first_name', read_only=True)
    user_lastname = serializers.EmailField(source='user.last_name', read_only=True)
    company_name = serializers.EmailField(source='user.company', read_only=True)
    department_name = serializers.CharField(source='department_name.department_name', read_only=True)
    
    class Meta:
        model = File_Document
        fields = (
            'id',
            'user',
            'user_email',
            'user_firstname',
            'user_lastname',
            'company_name',
            'department_name',
            'document_type',
            'agency',
            'upload_file',
            'renewal_date',
            'expiry_date',
        )

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = (
            'id',
            'company',
            'department_name',
        )

class FileLogSerializer(serializers.ModelSerializer):
    user_firstname = serializers.EmailField(source='user.first_name', read_only=True)
    user_lastname = serializers.EmailField(source='user.last_name', read_only=True)
    document_type = serializers.CharField(source='file_document.document_type', read_only=True)
    class Meta:
        model = FileLog
        fields = (
            'id',
            'user',
            'user_firstname',
            'user_lastname',
            'document_type',
            'file_document',
            'action',
            'timestamp', 
        )