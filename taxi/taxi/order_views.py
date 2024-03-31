from django.shortcuts import render, redirect

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages

from .models import Driver, Client, Order



class OrderMarketListView(ListView):
    model = Order
    template_name = 'taxi/order_market_list.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(status='Новый')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not Driver.objects.filter(user=request.user).exists():
            return redirect('driver_register')
        return super().dispatch(request, *args, **kwargs)


class OrderMarketDetailView(DetailView):
    model = Order
    template_name = 'taxi/order_market_detail.html'
    context_object_name = 'order'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not Driver.objects.filter(user=request.user).exists():
            return redirect('driver_register')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        User = get_user_model()
        user = User.objects.get(email=self.request.user)
        driver = Driver.objects.get(user=user)
        context['driver'] = driver
        return context


class DriverOrderListView(ListView):
    model = Order
    template_name = 'taxi/driver_orders.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        User = get_user_model()
        user = User.objects.get(email=self.request.user)
        driver = Driver.objects.get(user=user)
        return Order.objects.filter(driver=driver)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        User = get_user_model()
        user = User.objects.get(email=self.request.user)
        driver = Driver.objects.get(user=user)
        context['driver'] = driver
        return context
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not Driver.objects.filter(user=request.user).exists():
            return redirect('driver_register')
        return super().dispatch(request, *args, **kwargs)


class DriverOrderDetailView(DetailView):
    model = Order
    template_name = 'taxi/driver_order_detail.html'
    context_object_name = 'order'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not Driver.objects.filter(user=request.user).exists():
            return redirect('driver_register')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        User = get_user_model()
        user = User.objects.get(email=self.request.user)
        driver = Driver.objects.get(user=user)
        context['driver'] = driver
        return context


class ClientOrderListView(ListView):
    model = Order
    template_name = 'taxi/client_orders.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        User = get_user_model()
        user = User.objects.get(email=self.request.user)
        client = Client.objects.get(user=user)
        return Order.objects.filter(client=client)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        User = get_user_model()
        user = User.objects.get(email=self.request.user)
        client = Client.objects.get(user=user)
        context['client'] = client
        return context
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not Client.objects.filter(user=request.user).exists():
            return redirect('client_register')
        return super().dispatch(request, *args, **kwargs)

class ClientOrderDetailView(DetailView):
    model = Order
    template_name = 'taxi/client_order_detail.html'
    context_object_name = 'order'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not Client.objects.filter(user=request.user).exists():
            return redirect('client_register')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        User = get_user_model()
        user = User.objects.get(email=self.request.user)
        client = Client.objects.get(user=user)
        context['client'] = client
        return context
    
    def get_queryset(self):
        User = get_user_model()
        user = User.objects.get(email=self.request.user)
        client = Client.objects.get(user=user)
        return Order.objects.filter(client=client)


@login_required
def client_order_cancel(request, pk):
    User = get_user_model()
    user = User.objects.get(email=request.user)
    client = Client.objects.get(user=user)
    if not client:
        messages.error(request, 'Клиент не найден')
        return redirect('client_register')
    if not Order.objects.filter(id=pk).exists():
        messages.error(request, 'Заказ не найден')
        return redirect('orders_client_list')
    
    order = Order.objects.get(pk=pk)

    if order.client != client:
        messages.error(request, 'Вы не можете отменить этот заказ')
        return redirect('orders_client_list')
    
    if order.status == 'Отменен':
        messages.error(request, 'Заказ уже был отменен')
        return redirect('orders_client_list')
    
    order.status = 'Отменен'
    order.save()
    messages.success(request, 'Заказ успешно отменен')
    return redirect('orders_client_list')


@login_required
def driver_order_accept(request, pk):
    User = get_user_model()
    user = User.objects.get(email=request.user)
    driver = Driver.objects.get(user=user)
    if not driver:
        print("DRIVER NOT FOUND")
        messages.error(request, 'Водитель не найден')
        return redirect('driver_register')
    if not Order.objects.filter(id=pk).exists():
        print("ORDER DOES NOT EXSIST")
        messages.error(request, 'Заказ не найден')
        return redirect('orders_driver_list')

    order = Order.objects.get(pk=pk)

    if order.driver:
        print("ORDER ALREADY HAS DRIVER")
        messages.error(request, 'Вы не можете принять этот заказ')
        return redirect('orders_driver_list')
    
    if not driver.verified:
        print("DRIVER IS NOT VERIFIED")
        messages.error(request, 'Водитель не подтвержден')
        return redirect('orders_driver_list')
    
    if order.car_type != driver.car_type:
        print("CAR TYPES DO NOT MATCH")
        messages.error(request, 'Типы транспорта не совпадают')
        return redirect('orders_driver_list')
    
    if order.status != 'Новый':
        print("ORDER IS ALREADY PROCESSING")
        messages.error(request, 'Заказ уже был принят')
        return redirect('orders_driver_list')

    order.status = 'Принят'
    order.driver = driver
    order.save()
    messages.success(request, 'Заказ успешно принят')
    print("ORDER SUCCESSFULLY RECEIVED")
    return redirect('orders_driver_list')

@login_required
def driver_order_complete(request, pk):
    User = get_user_model()
    user = User.objects.get(email=request.user)
    driver = Driver.objects.get(user=user)
    if not driver:
        messages.error(request, 'Водитель не найден')
        return redirect('driver_register')
    if not Order.objects.filter(id=pk).exists():
        messages.error(request, 'Заказ не найден')
        return redirect('orders_driver_list')

    order = Order.objects.get(pk=pk)

    if order.driver != driver:
        messages.error(request, 'Вы не можете завершить этот заказ')
        return redirect('orders_driver_list')
    
    if order.status == 'Завершен':
        messages.error(request, 'Заказ уже был завершен')
        return redirect('orders_driver_list')

    order.status = 'Завершен'
    order.save()
    messages.success(request, 'Заказ успешно завершен')
    return redirect('orders_driver_list')