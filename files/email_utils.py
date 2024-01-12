from django.core.mail import send_mail
from django.conf import settings

from .models import File_Document, Person_Document

def send_notification_email(document, recipient_email, is_admin=False, message=None):
    subject = 'Document Renewal Reminder'
    
    if is_admin:
       message = f'The document from the company {document.user.company}, {document.department_name} department, which is a {document.get_document_type_display()} document, created by {document.user.first_name} {document.user.last_name}, has expired. Please take action.'
    elif message is None:
        message = f'The document from the company {document.user.company}, {document.department_name} department, which is a {document.get_document_type_display()} document, is expiring soon. Please renew it.'
    
    from_email = settings.EMAIL_HOST_USER 
    recipient_list = [recipient_email]
    send_mail(subject, message, from_email, recipient_list)


def send_person_notification_email(document, recipient_email, is_admin=False, message=None):
    subject = 'License Renewal Reminder'
    
    if isinstance(document, File_Document):
        # Logic for File_Document
        if is_admin:
            message = f'The document from the company {document.user.company}, {document.department_name} department, which is a {document.get_document_type_display()} document, created by {document.user.first_name} {document.user.last_name}, has expired. Please take action.'
        elif message is None:
            message = f'The document from the company {document.user.company}, {document.department_name} department, which is a {document.get_document_type_display()} document, is expiring soon. Please renew it.'
    elif isinstance(document, Person_Document):
        # Logic for Person_Document
        if is_admin:
            message = f'The person License for {document.person_fullname} created by {document.user.first_name} {document.user.last_name}, has expired. Please take action.'
        elif message is None:
            message = f'The person License for {document.person_fullname} is expiring soon. Please renew it.'
    else:
        raise ValueError("Unsupported License type")

    from_email = settings.EMAIL_HOST_USER 
    recipient_list = [recipient_email]
    send_mail(subject, message, from_email, recipient_list)
