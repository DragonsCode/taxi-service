from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path 
from . import views 

urlpatterns = [ 
    path('', views.index, name='index'),
    path('login/', LoginView.as_view(template_name='taxi/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='taxi/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('register/client/', views.client_register, name='register_client'),
    path('register/driver/', views.driver_register, name='register_driver'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/profile/client/', views.client_profile, name='client_profile'),
    path('accounts/profile/driver/', views.driver_profile, name='driver_profile'),
]