from django.db import models
from files.models import File_Document, Person_Document
from django.utils import timezone
from datetime import timedelta
import os


def get_upload_path(instance, filename):
    return os.path.basename(filename)

# Create your models here.
class Receipt(models.Model):
    file = models.ForeignKey(File_Document, on_delete=models.CASCADE,default=1,related_name='receipt_set')
    fined = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    receipt = models.FileField(upload_to=get_upload_path,  null=True, blank=True)
    invoice_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        current_utc_time = timezone.now()
        time_difference = timedelta(hours=8) 

        self.invoice_date = current_utc_time + time_difference

        super().save(*args, **kwargs)

    def __str__(self):
        return f"File Document {self.file} - {self.file.document_type} - {self.file.expiry_date}"
    

class Person_Receipt(models.Model):
    person_document = models.ForeignKey(Person_Document, on_delete=models.CASCADE,default=1,related_name='receipts')
    fined = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    receipt = models.FileField(upload_to=get_upload_path,  null=True, blank=True)
    invoice_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        current_utc_time = timezone.now()
        time_difference = timedelta(hours=8) 

        self.invoice_date = current_utc_time + time_difference

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Person Document {self.person_document} - {self.person_document.document_type} - {self.person_document.expiry_date} - {self.person_document.person_fullname or 'No Name'}"
    
    