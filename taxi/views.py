from django.http import HttpResponse

from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from .forms import DriverRegistrationForm, ClientRegistrationForm
from .models import Driver, Client

def driver_register(request):
    if request.method == 'POST':
        form = DriverRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            driver = Driver.objects.create(user=user, **form.cleaned_data)
            login(request, user)
            return redirect('index')
    else:
        form = DriverRegistrationForm()
    return render(request, 'register_driver.html', {'form': form})

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