from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib import messages

from django.shortcuts import render, redirect

from .forms import DriverRegistrationForm, ClientRegistrationForm
from .models import Driver, Client


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
    return render(request, 'driver_profile.html', context)

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
    return render(request, 'client_profile.html', context)

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

    return render(request, 'register_driver.html', {'form': user_form})

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

    return render(request, 'register_client.html', {'form': user_form})

def register(request):
    return render(request, 'register.html')

def index(request):
    context = {}
    return render(request, 'index.html', context)