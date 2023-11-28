from django.urls import path,include
from . import views

from .views import (
        Receipt_view
)

urlpatterns = [
    path('',include([
        #api for files
        path('', Receipt_view.as_view({
            'get': 'list',
            'post': 'create',
        })),
        path('<int:pk>/', Receipt_view.as_view({
            'put': 'update',
            'delete': 'destroy',
        })),
          path('receipt/', Receipt_view.as_view({
            'get': 'receipt',  # Custom action for expired files
        })),
    ])),

path('create_receipt/<int:file_id>/', views.create_receipt, name='create_receipt'),
path('receipt_valid_documents/', views.receipt_valid_documents, name='receipt_valid_documents'),
path('admin_receipt_documents/', views.admin_receipt_documents, name='admin_receipt_documents'),

]