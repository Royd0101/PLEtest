from django.urls import path,include
from . import views

from .views import (
    File_Document_view, Department_view,FileLog_view
)

urlpatterns = [
    path('',include([
        #api for files
        path('', File_Document_view.as_view({
            'get': 'list',
            'post': 'create',
        })),
        path('<int:pk>/', File_Document_view.as_view({
            'put': 'update',
            'delete': 'destroy',
        })),
        

        #api for department
        path('department/', Department_view.as_view({'get': 'list', 'post': 'create'}), name='department-list'),
        path('department/<int:pk>/', Department_view.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='department-detail'),
        
        #api for logs
        path('logs/', FileLog_view.as_view({'get': 'list', 'post': 'create'}), name='department-list'),
        path('logs/<int:pk>/', FileLog_view.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='department-detail'),

        #custom api for user get list of data created by user
        path('expired/', File_Document_view.as_view({
            'get': 'expired',  # Custom action for expired files
        })),
        path('valid_file/', File_Document_view.as_view({
            'get': 'valid_file',  # Custom action for valid files
        })),
        path('to_be_renew/', File_Document_view.as_view({
            'get': 'to_be_renew',  # Custom action for files to be renewed
        })),  

        #custom api for admin will get all data 
        path('expired_documents/', File_Document_view.as_view({
            'get': 'admin_expired_list',  # Custom action for expired files
        })),
        path('valid_documents/', File_Document_view.as_view({
            'get': 'admin_valid_list',  # Custom action for valid files
        })),
        path('renewal_documents/', File_Document_view.as_view({
            'get': 'admin_to_be_renew_list',  # Custom action for files to be renewed
        })), 
    ])),

    #create new file page
    path('create_new_file_form/', views.create_new_file_form, name='create_new_file_form'),
    #department page
    path('department_page/', views.department_page, name='department_page'),
    #renew file page
    path('renew_file_form/<int:file_id>/', views.renew_file_form, name='renew_file_form'),
    #file profile page
    path('display_file_page/<int:file_id>/', views.display_file_page, name='display_file_page'),
    #user logs
    path('users_logs/', views.users_logs, name='users_logs'),


    #render admin page for dashboard
    path('admin_expired/', views.display_admin_expired, name='admin_expired'),
    path('admin_valid/', views.display_admin_valid, name='admin_valid'),
    path('admin_to_be_renew/', views.display_admin_to_be_renew, name='admin_to_be_renew'),
    path('department_list/', views.department_list, name='department_list'),
    path('create_department/', views.create_department, name='create_department'),
    path('update_department/<int:department_id>/', views.update_department, name='update_department'),
    path('delete_department/<int:department_id>/', views.delete_department, name='delete_department'),



    #api
    #create new file api
    path('create_new_file/', views.create_new_file, name='create_new_file'),
    #get renew file list
    path('get_renew_file_list/', views.get_renew_file_list, name='get_renew_file_list'),
    #get expired file list
    path('get_expired_file_list/', views.get_expired_file_list, name='get_expired_file_list'),
    #get valid file list
    path('get_valid_file_list/', views.get_valid_file_list, name='get_valid_file_list'),
    #renew_file_api
    path('renew_file/<int:file_id>/', views.renew_file, name='renew_file'),



]
