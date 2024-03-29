
from django.utils import timezone
from .models import File_Document,Person_Document
from users.models import User
from django.utils import timezone
from celery import shared_task
from .email_utils import send_notification_email,send_person_notification_email

shared_task
def check_document_expiry():
    admin_user = User.objects.get(is_superuser=True)
    admin_email = admin_user.email

    expiration_threshold = timezone.now() + timezone.timedelta(days=60)
    expiring_documents = File_Document.objects.filter(expiry_date__lte=expiration_threshold)

    for document in expiring_documents:
        expiry_datetime = timezone.make_aware(timezone.datetime(
            document.expiry_date.year,
            document.expiry_date.month,
            document.expiry_date.day
        ))

        two_months_before_expiry = expiry_datetime - timezone.timedelta(days=60)

        if timezone.now() >= two_months_before_expiry and timezone.now() < expiry_datetime:
            user_message = f'The document from the company {document.user.company}, {document.department_name} department, which is a {document.get_document_type_display()} document, is expiring soon. Please renew it.'
            send_notification_email(document, document.user.email, message=user_message)

        elif timezone.now() >= expiry_datetime:
            user_message = f'The document from the company {document.user.company}, {document.department_name} department, which is a {document.get_document_type_display()} document, has expired. Please take action.'
            send_notification_email(document, document.user.email, message=user_message)

            admin_message = f'The document "{document.get_document_type_display()}" created by {document.user.first_name} {document.user.last_name} has expired. Please take action.'
            send_notification_email(document, admin_email, is_admin=True, message=admin_message)

    return "Notifications sent successfully."


@shared_task
def check_person_document_expiry():
    admin_user, _ = User.objects.get_or_create(is_superuser=True)
    admin_email = admin_user.email

    expiration_threshold = timezone.now() + timezone.timedelta(days=60)
    expiring_person_documents = Person_Document.objects.filter(expiry_date__lte=expiration_threshold)

    for person_document in expiring_person_documents:
        expiry_datetime = timezone.make_aware(timezone.datetime(
            person_document.expiry_date.year,
            person_document.expiry_date.month,
            person_document.expiry_date.day
        ))

        two_months_before_expiry = expiry_datetime - timezone.timedelta(days=60)

        if timezone.now() >= two_months_before_expiry and timezone.now() < expiry_datetime:
            user_message = f'The person document for {person_document.person_fullname} is expiring soon. Please renew it.'
            send_person_notification_email(person_document, person_document.user.email, message=user_message)

        elif timezone.now() >= expiry_datetime:
            user_message = f'The person document for {person_document.person_fullname} has expired. Please take action.'
            send_person_notification_email(person_document, person_document.user.email, message=user_message)

            admin_message = f'The person document for {person_document.person_fullname} has expired. Please take action.'
            send_person_notification_email(person_document, admin_email, is_admin=True, message=admin_message)

    return "Person document notifications sent successfully."