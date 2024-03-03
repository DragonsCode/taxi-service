from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path 
from . import views 

urlpatterns = [ 
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('user_agreement/', views.user_agreement, name='user_agreement'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),

    path('login/', LoginView.as_view(template_name='taxi/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='taxi/logout.html'), name='logout'),

    path('register/', views.register, name='register'),
    path('register/client/', views.client_register, name='register_client'),
    path('register/driver/', views.driver_register, name='register_driver'),

    path('profile/', views.profile, name='profile'),
    path('profile/client/', views.client_profile, name='client_profile'),
    path('profile/driver/', views.driver_profile, name='driver_profile'),

    path('orders/market/', views.OrderMarketListView.as_view(), name='orders_market_list'),
    path('orders/market/<int:pk>/', views.OrderMarketDetailView.as_view(), name='order_market_detail'),

    path('orders/client/', views.ClientOrderListView.as_view(), name='orders_client_list'),
    path('orders/client/<int:pk>/', views.ClientOrderDetailView.as_view(), name='order_client_detail'),

    path('orders/driver/', views.DriverOrderListView.as_view(), name='orders_driver_list'),
    path('orders/driver/<int:pk>/', views.DriverOrderDetailView.as_view(), name='order_driver_detail'),

    path('orders/driver/accept/<int:pk>/', views.driver_order_accept, name='driver_order_accept'),
    path('orders/driver/complete/<int:pk>/', views.driver_order_complete, name='driver_order_complete'),

    path('orders/client/cancel/<int:pk>/', views.client_order_cancel, name='client_order_cancel'),
]