from rest_framework import serializers
from files.models import File_Document, Department,FileLog


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = (
            'id',
            'company',
            'department_name',
        )
        
class FileSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_firstname = serializers.EmailField(source='user.first_name', read_only=True)
    user_lastname = serializers.EmailField(source='user.last_name', read_only=True)
    department_name = serializers.CharField(source='department_name.department_name', read_only=True)
    company_name = serializers.EmailField(source='user.company', read_only=True)

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



class FileLogSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.EmailField(source='user.first_name', read_only=True)
    last_name = serializers.EmailField(source='user.last_name', read_only=True)
    file_name = serializers.EmailField(source='file.document_type', read_only=True)
    company_name = serializers.EmailField(source='file.company', read_only=True)
    department_name = serializers.EmailField(source='file.department_name', read_only=True)
    previous_file_name = serializers.EmailField(source='previous_file.upload_file', read_only=True)
    current_file_name = serializers.EmailField(source='file.upload_file', read_only=True)
    class Meta:
        model = FileLog
        fields = (
            'id',
            'user_email',
            'first_name',
            'last_name',
            'file_name',
            'file',
            'company_name',
            'department_name',
            'action',
            'timestamp', 
            'previous_file_name',
            'current_file_name',
        )