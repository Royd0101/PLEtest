from django.db import models
from django.utils import timezone
from datetime import timedelta
import os
# Create your models here.



def get_upload_path(instance, filename):
    return os.path.basename(filename)

class Department(models.Model):
    department_name = models.CharField(max_length=50, null=True)
    company = models.ForeignKey('users.Company', on_delete=models.CASCADE)

    def __str__(self):
        return self.department_name
    
    class Meta:
        unique_together = ('department_name', 'company')

class File_Document(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    company = models.ForeignKey('users.Company', on_delete=models.CASCADE, default=1) 
    department_name = models.ForeignKey(Department, on_delete=models.CASCADE, default=1)

    document_type = models.CharField(max_length=50)
    agency = models.CharField(max_length=50, default='Default Agency Name')
    upload_file = models.FileField(upload_to=get_upload_path)
    renewal_date = models.DateField()
    expiry_date = models.DateField()

    def __str__(self):
        return f"File Document {self.user} - {self.document_type} - {self.expiry_date}"
    
    def delete(self):
        self.upload_file.delete()
        super().delete()

class Person_Document(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    person_fullname = models.CharField(max_length=50)
    document_type = models.CharField(max_length=50)
    upload_file = models.FileField(upload_to=get_upload_path)
    renewal_date = models.DateField()
    expiry_date = models.DateField()

    def __str__(self):
        return f"Person Document {self.user} - {self.document_type} - {self.expiry_date} - {self.person_fullname or 'No Name'}"
    
    def delete(self):
        self.upload_file.delete()
        super().delete()

class FileLog(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    file = models.ForeignKey(File_Document, on_delete=models.CASCADE, related_name='file_logs')  
    previous_file = models.FileField(upload_to=get_upload_path, null=True, blank=True)
    expiry_date = models.DateField(default=None, null=True, blank=True)
    action = models.CharField(max_length=50)
    timestamp = models.DateTimeField()

    def save(self, *args, **kwargs):
        current_utc_time = timezone.now()
        time_difference = timedelta(hours=8) 

        self.timestamp = current_utc_time + time_difference

        super().save(*args, **kwargs)

    def __str__(self):
        return f" {self.action} {self.file.document_type}"
    
class PersonLog(models.Model):
    person = models.ForeignKey(Person_Document, on_delete=models.CASCADE, related_name='person_logs')  
    previous_file = models.FileField(upload_to=get_upload_path, null=True, blank=True)
    expiry_date = models.DateField(default=None, null=True, blank=True)
    action = models.CharField(max_length=50)
    timestamp = models.DateTimeField()

    def save(self, *args, **kwargs):
        current_utc_time = timezone.now()
        time_difference = timedelta(hours=8) 

        self.timestamp = current_utc_time + time_difference

        super().save(*args, **kwargs)

    def __str__(self):
        return f" {self.action} {self.person.document_type}"