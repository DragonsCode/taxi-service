from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path 
from . import views 

urlpatterns = [ 
    path('', views.index, name='index'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('register/client/', views.client_register, name='register_client'),
    path('register/driver/', views.driver_register, name='register_driver'),
]