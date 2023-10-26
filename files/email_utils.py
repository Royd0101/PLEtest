from django.core.mail import send_mail
from decouple import config

def send_notification_email(document, recipient_email, is_admin=False):
    subject = f'Document Renewal Reminder'
    
    if is_admin:
        message = f'The document "{document.select_BU} - {document.document_type}" has expired. Please take action.'
    else:
        message = f'The document "{document.select_BU} - {document.document_type}" is expiring soon. Please renew it.'
    
    from_email = config('EMAIL_HOST_USER')
    recipient_list = [recipient_email]
    send_mail(subject, message, from_email, recipient_list)