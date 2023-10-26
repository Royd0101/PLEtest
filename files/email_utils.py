from django.core.mail import send_mail
from django.conf import settings

def send_notification_email(document, recipient_email, is_admin=False, message=None):
    subject = f'Document Renewal Reminder'
    
    if is_admin:
       message = f'The document from the company {document.user.company}, {document.department_name} department, which is a {document.get_document_type_display()} document, created by {document.user.first_name} {document.user.last_name}, has expired. Please take action.'
    elif message is None:
        message = f'The document from the company {document.user.company}, {document.department_name} department, which is a {document.get_document_type_display()} document,is expiring soon. Please renew it.'
    
    from_email = settings.EMAIL_HOST_USER 
    recipient_list = [recipient_email]
    send_mail(subject, message, from_email, recipient_list)