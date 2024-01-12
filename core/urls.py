"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings  
from django.conf.urls.static import static 
from django.contrib import admin
from django.urls import path, include
from users.views import dashboard, create_user, create_user_page, user_list, update_users,redirect_to_login, login_user, login_page, logout_user,company_page,create_company,company_list,delete_user, delete_company,department_total_fine,update_company
from files.views import create_new_file_form,create_new_file, renew_file_form ,get_expired_file_list, get_renew_file_list,renew_file,department_page,department_list,create_department,display_file_page,admin_logs,update_department,delete_department,automatic_send_mail,user_logs,admin_expired_file_list,admin_valid_file_list,admin_renew_file_list,file_documents_with_receipts,create_person_documents,  expired_person_document_list,renew_person_document_list,get_expired_person_list,get_renew_person_list,get_valid_person_list,renew_person_documents,person_documents_with_receipts,admin_person_logs,person_logs,yearly_expired_license,yearly_expired_files_by_month,admin_yearly_expired_license,valid_person_document_list
from receipt.views import create_receipt,receipt_valid_documents,admin_receipt_documents,create_person_receipt,admin_person_receipt_documents,person_receipt_documents
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('users/', include('users.urls')),
        path('file/', include('files.urls')),
        path('receipts/', include('receipt.urls')),
    ])),

    #pages
    path('', redirect_to_login, name='root'),
    #Display login page
    path('login_page/', login_page, name='login_page'),
    #Display dashboard
    path('dashboard/', dashboard, name='dashboard'),
    #Display create user page
    path('create_user_page/', create_user_page, name='create_user_page'),
    #Display user list page
    path('user_list/', user_list, name='user_list'),
    #Create new file page
    path('create_new_file_form/', create_new_file_form, name='create_new_file_form'),
    #renew file page
    path('renew_file_form/', renew_file_form, name='renew_file_form'),
    #company page
    path('company_page/', company_page, name='company_page'),
    #department
    path('department_page/', department_page, name='department_page'),
    #create company
    path('create_company/', create_company, name='create_company'),
    #delete company
    path('delete_company/', delete_company, name='delete_company'),
    #delete company
    path('update_company/', update_company, name='update_company'),
    #company_list
    path('company_list/', company_list, name='company_list'),
    #department_list
    path('department_list/', department_list, name='department_list'),
    #create department
    path('create_department/', create_department, name='create_department'),
    #display file profile
    path('display_file_page/', display_file_page, name='display_file_page'),
    #file logs
    path('admin_logs/', admin_logs, name='admin_logs'),
    path('user_logs/',user_logs, name='user_logs'),
    #person logs
    path('admin_person_logs/', admin_person_logs, name='admin_person_logs'),
    path('person_logs/', person_logs, name='person_logs'),
    #update department
    path('update_department/', update_department, name='update_department'),
    #delete department
    path('delete_department/', delete_department, name='delete_department'),



    #functions
    #user
    #login user api function
    path('login_user/', login_user, name='login_user'),
    path('logout_user/', logout_user, name='logout_user'),
    #create user api function
    path('create_user/', create_user, name='create_user'),
    #update user api
    path('update_users/', update_users, name='update_users'),
    #delete user
    path('delete_user/', delete_user, name='delete_user'),


    #file
    #create file api function
    path('create_new_file/', create_new_file, name='create_new_file'),
    
    #get expired list api
    path('get_expired_file_list/', get_expired_file_list, name='get_expired_file_list'),
    #get renew list api
    path('get_renew_file_list/', get_renew_file_list, name='get_renew_file_list'),
    #renew document api
    path('renew_file/', renew_file, name='renew_file'),

        #admin 
    path('admin_expired_list/', admin_expired_file_list, name='admin_expired_list'),
    path('admin_valid_list', admin_valid_file_list, name='admin_valid_list'),
    path('admin_renew_list', admin_renew_file_list, name='admin_renew_list'),


    #sending email
    path('automatic_send_mail/', automatic_send_mail, name='automatic_send_mail'),


    #receipt
    path('create_receipt/', create_receipt, name='create_receipt'),
    path('create_person_receipt/<int:file_id>/', create_person_receipt, name='create_person_receipt'),
    path('receipt_valid_documents/', receipt_valid_documents, name='receipt_valid_documents'),
    path('admin_receipt_documents/', admin_receipt_documents, name='admin_receipt_documents'),

    path('file_documents_with_receipts', file_documents_with_receipts, name='file_documents_with_receipts'),
    path('person_documents_with_receipts', person_documents_with_receipts, name='person_documents_with_receipts'),

    #USER CHART
    path('department_total_fine/', department_total_fine, name='department_total_fine'),
    
    #create person documents
    path('person_documents/', create_person_documents, name='person_documents'),
    #admin person documents
    path('admin_person_expired_list/', expired_person_document_list, name='admin_person_expired_list'),
    path('admin_person_renew_list', renew_person_document_list, name='admin_person_renew_list'),
    
    path('valid_person_document_list', valid_person_document_list, name='valid_person_document_list'),

    #user person documents
    path('get_expired_person_list/', get_expired_person_list, name='get_expired_person_list'),
    path('get_renew_person_list', get_renew_person_list, name='get_renew_person_list'),
    path('get_valid_person_list', get_valid_person_list, name='get_valid_person_list'),
    path('renew_person_documents/', renew_person_documents, name='renew_person_documents'),

    path('admin_person_receipt_documents/', admin_person_receipt_documents, name='admin_person_receipt_documents'),
    path('person_receipt_documents/', person_receipt_documents, name='person_receipt_documents'),

    
    path('admin_yearly_expired_license/', admin_yearly_expired_license, name='admin_yearly_expired_license'),
    path('yearly_expired_license/', yearly_expired_license, name='yearly_expired_license'),
    path('yearly_expired_files_by_month/', yearly_expired_files_by_month, name='yearly_expired_files_by_month'),

  
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

