from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib import messages

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.shortcuts import render, redirect

from .forms import DriverRegistrationForm, ClientRegistrationForm
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
        return redirect('client_orders')
    
    order = Order.objects.get(pk=pk)

    if order.client != client:
        messages.error(request, 'Вы не можете отменить этот заказ')
        return redirect('client_orders')
    
    if order.status == 'Отменен':
        messages.error(request, 'Заказ уже был отменен')
        return redirect('client_orders')
    
    order.status = 'Отменен'
    order.save()
    messages.success(request, 'Заказ успешно отменен')
    return redirect('client_orders')


@login_required
def driver_order_accept(request, pk):
    User = get_user_model()
    user = User.objects.get(email=request.user)
    driver = Driver.objects.get(user=user)
    if not driver:
        messages.error(request, 'Водитель не найден')
        return redirect('driver_register')
    if not Order.objects.filter(id=pk).exists():
        messages.error(request, 'Заказ не найден')
        return redirect('driver_orders')

    order = Order.objects.get(pk=pk)

    if order.driver:
        messages.error(request, 'Вы не можете принять этот заказ')
        return redirect('driver_orders')
    
    if order.status != 'Новый':
        messages.error(request, 'Заказ уже был принят')
        return redirect('driver_orders')

    order.status = 'Принят'
    order.save()
    messages.success(request, 'Заказ успешно принят')
    return redirect('driver_orders')

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
        return redirect('driver_orders')

    order = Order.objects.get(pk=pk)

    if order.driver != driver:
        messages.error(request, 'Вы не можете завершить этот заказ')
        return redirect('driver_orders')
    
    if order.status == 'Завершен':
        messages.error(request, 'Заказ уже был завершен')
        return redirect('driver_orders')

    order.status = 'Завершен'
    order.save()
    messages.success(request, 'Заказ успешно завершен')
    return redirect('driver_orders')

@login_required
def profile(request):
    User = get_user_model()
    user = User.objects.get(email=request.user)
    try:
        client = Client.objects.get(user=user)
    except:
        client = None
    try:
        driver = Driver.objects.get(user=user)
    except:
        driver = None
    if client:
        return redirect('client_profile')
    elif driver:
        return redirect('driver_profile')
    else:
        return redirect('register')

@login_required
def driver_profile(request):
    User = get_user_model()
    user = User.objects.get(email=request.user)
    driver = Driver.objects.get(user=user)
    if not driver:
        messages.error(request, 'Driver profile not found')
        return redirect('driver_register')
    context = {
        'driver': driver
    }
    return render(request, 'taxi/driver_profile.html', context)

@login_required
def client_profile(request):
    User = get_user_model()
    user = User.objects.get(email=request.user)
    client = Client.objects.get(user=user)
    if not client:
        messages.error(request, 'Client profile not found')
        return redirect('client_register')
    context = {
        'client': client
    }
    return render(request, 'taxi/client_profile.html', context)

def driver_register(request):
    if request.method == 'POST':
        user_form = DriverRegistrationForm(request.POST)
        if user_form.is_valid():
            # Separate user and driver data extraction for clarity:
            user_data = {
                'first_name': user_form.cleaned_data['first_name'],
                'last_name': user_form.cleaned_data['last_name'],
                'email': user_form.cleaned_data['email'],
                'password': user_form.cleaned_data['password1'],
                # ... other user-specific fields from form.cleaned_data
            }
            driver_data = {
                'middle_name': user_form.cleaned_data['middle_name'],
                'phone': user_form.cleaned_data['phone'],
                'photo': user_form.cleaned_data['photo'],
                'car': user_form.cleaned_data['car'],
                'car_photo': user_form.cleaned_data['car_photo'],
                'passport_photo': user_form.cleaned_data['passport_photo'],
                'insurance_photo': user_form.cleaned_data['insurance_photo'],
                'license_photo': user_form.cleaned_data['license_photo'],
                'description': user_form.cleaned_data['description'],
                'car_type': user_form.cleaned_data['car_type'],
                'experience': user_form.cleaned_data['experience'],
                # ... other driver-specific fields from form.cleaned_data
            }

            # Create user object, ensuring secure password handling:
            User = get_user_model()
            user = User.objects.create_user(**user_data)
            user.set_password(user_data['password'])  # Set password securely
            user.save()

            # Create driver object associated with the user:
            driver = Driver.objects.create(user=user, **driver_data)

            # Log in the user after successful registration:
            login(request, user)
            return redirect('index')  # Replace with your desired redirect url
    else:
        user_form = DriverRegistrationForm()

    return render(request, 'taxi/register_driver.html', {'form': user_form})

def client_register(request):
    if request.method == 'POST':
        user_form = ClientRegistrationForm(request.POST)
        if user_form.is_valid():
            # Separate user and client data extraction for clarity:
            user_data = {
                'first_name': user_form.cleaned_data['first_name'],
                'last_name': user_form.cleaned_data['last_name'],
                'email': user_form.cleaned_data['email'],
                'password': user_form.cleaned_data['password1'],
                # ... other user-specific fields from form.cleaned_data
            }
            client_data = {
                'middle_name': user_form.cleaned_data['middle_name'],
                'phone': user_form.cleaned_data['phone'],
                'photo': user_form.cleaned_data['photo'],
                # ... other client-specific fields from form.cleaned_data
            }

            # Create user object, ensuring secure password handling:
            User = get_user_model()
            user = User.objects.create_user(**user_data)
            user.set_password(user_data['password'])  # Set password securely
            user.save()

            # Create client object associated with the user:
            client = Client.objects.create(user=user, **client_data)

            # Log in the user after successful registration:
            login(request, user)
            return redirect('index')  # Replace with your desired redirect url
    else:
        user_form = ClientRegistrationForm()

    return render(request, 'taxi/register_client.html', {'form': user_form})

def register(request):
    return render(request, 'taxi/register.html')

def index(request):
    context = {}
    return render(request, 'taxi/index.html', context)

def about(request):
    context = {}
    return render(request, 'taxi/about.html', context)

def user_agreement(request):
    context = {}
    return render(request, 'taxi/user_agreement.html', context)

def privacy_policy(request):
    context = {}
    return render(request, 'taxi/privacy_policy.html', context)