from django.contrib import admin

from .models import File_Document , Department,FileLog
# Register your models here.
@admin.register(File_Document)
class File_Document_Admin(admin.ModelAdmin):
    search_fields = ('id', 'email',)
    list_display = ('id','department_name','document_type','renewal_date', 'expiry_date')

@admin.register(Department)
class Department_Admin(admin.ModelAdmin):
    search_fields = ('id', 'department_name',)
    list_display = ('id','department_name')

@admin.register(FileLog)
class Department_Admin(admin.ModelAdmin):
    search_fields = ('id', 'action','user','timestamp')
    list_display = ('id','user','file_document','action','timestamp')