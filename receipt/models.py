from django.db import models
from files.models import File_Document
import os


def get_upload_path(instance, filename):
    return os.path.basename(filename)

# Create your models here.
class Receipt(models.Model):
    file = models.ForeignKey(File_Document, on_delete=models.CASCADE,default=1)
    fined = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    receipt = models.FileField(upload_to=get_upload_path,  null=True, blank=True)
    
    