from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path 
from . import views, order_views, driver_views, client_views

urlpatterns = [ 
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('user_agreement/', views.user_agreement, name='user_agreement'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),

    path('login/', LoginView.as_view(template_name='taxi/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='taxi/logout.html'), name='logout'),

    path('register/', views.register, name='register'),
    path('register/client/', client_views.client_register, name='register_client'),
    path('register/driver/', driver_views.driver_register, name='register_driver'),

    path('profile/', views.profile, name='profile'),
    path('profile/client/', client_views.client_profile, name='client_profile'),
    path('profile/driver/', driver_views.driver_profile, name='driver_profile'),

    path('orders/market/', order_views.OrderMarketListView.as_view(), name='orders_market_list'),
    path('orders/market/<int:pk>/', order_views.OrderMarketDetailView.as_view(), name='order_market_detail'),

    path('orders/client/', order_views.ClientOrderListView.as_view(), name='orders_client_list'),
    path('orders/client/<int:pk>/', order_views.ClientOrderDetailView.as_view(), name='order_client_detail'),

    path('orders/driver/', order_views.DriverOrderListView.as_view(), name='orders_driver_list'),
    path('orders/driver/<int:pk>/', order_views.DriverOrderDetailView.as_view(), name='order_driver_detail'),

    path('orders/driver/accept/<int:pk>/', order_views.driver_order_accept, name='driver_order_accept'),
    path('orders/driver/complete/<int:pk>/', order_views.driver_order_complete, name='driver_order_complete'),

    path('orders/client/cancel/<int:pk>/', order_views.client_order_cancel, name='client_order_cancel'),

    path('orders/new/', views.request_order, name='request_order'),

    path('route/', views.show_route, name='route'),
    path('calculate_price/', views.calculate_price, name='calculate_price'),
]