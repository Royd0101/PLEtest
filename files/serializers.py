from rest_framework import serializers
from files.models import File_Document, Department,FileLog

class FileSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_firstname = serializers.EmailField(source='user.first_name', read_only=True)
    user_lastname = serializers.EmailField(source='user.last_name', read_only=True)
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
    company_name = serializers.EmailField(source='company.company_name', read_only=True)
    class Meta:
        model = Department
        fields = (
            'id',
            'company',
            'department_name',
            'company_name',
        )

class FileLogSerializer(serializers.ModelSerializer):
    first_name = serializers.EmailField(source='user.first_name', read_only=True)
    last_name = serializers.EmailField(source='user.last_name', read_only=True)
    file = serializers.EmailField(source='file.document_type', read_only=True)
    class Meta:
        model = FileLog
        fields = (
            'id',
            'first_name',
            'last_name',
            'file',
            'action',
            'timestamp', 
        )