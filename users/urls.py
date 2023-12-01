from django.urls import path, include
from .views import Users, create_user, update_user, dashboard, create_user_page, user_list,redirect_to_login, login_user, login_page, logout_user, company_page,create_company,company_list,delete_user,delete_company


from .views import (
    Company_views
)

urlpatterns = [
    path('', include([
        path('', Users.as_view({
            'get': 'list',
            'post': 'create',
        })),
        path('<int:pk>/', Users.as_view({
             'get': 'retrieve',
            'put': 'update',
            'delete': 'destroy',
        })),

        path('company/', Company_views.as_view({'get': 'list', 'post': 'create'}), name='company-list'),
        path('company/<int:pk>/', Company_views.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='company-detail'),
    ])),
    
    #api
    #user Crud
    path('user_list/', user_list, name='user_list'),
    path('create_user/', create_user, name='create_user'),
    path('update_user/<int:user_id>/', update_user, name='update_user'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),

    path('login_user/', login_user, name='login_user'),
    path('logout_user/', logout_user, name='logout_user'),

    #company Crud
    path('create_company/', create_company, name='create_company'),
    path('delete_company/<int:company_id>/', delete_company, name='delete_company'),
    path('company_list/', company_list, name='company_list'),

    #pages
    path('redirect_to_login/', redirect_to_login, name='redirect_to_login'),
    path('login_page/', login_page, name='login_page'),
    path('dashboard/', dashboard, name='dashboard'),
    path('company_page/', company_page, name='company_page'),
    path('create_user_page/', create_user_page, name='create_user_page'),

   
]
