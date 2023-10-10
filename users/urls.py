from django.urls import path, include
from .views import Users, create_user, update_user, dashboard, create_user_page, user_list, update_user_page,redirect_to_login, login_user, login_page, logout_user
from django.contrib.auth import views as auth_views


from .views import (
    Company
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

        path('company/', Company.as_view({'get': 'list', 'post': 'create'}), name='company-list'),
        path('company/<int:pk>/', Company.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='company-detail'),
    ])),
    
    #api
    path('create_user/', create_user, name='create_user'),
    path('update_user/<int:user_id>/', update_user, name='update_user'),
    path('login_user/', login_user, name='login_user'),
    path('logout_user/', logout_user, name='logout_user'),

    #pages
    path('redirect_to_login/', redirect_to_login, name='redirect_to_login'),
     path('login_page/', login_page, name='login_page'),
    path('dashboard/', dashboard, name='dashboard'),
    path('create_user_page/', create_user_page, name='create_user_page'),
    path('user_list/', user_list, name='user_list'),
    path('update_user_page/<int:user_id>/', update_user_page, name='update_user_page'),
]
