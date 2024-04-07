from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib import messages

from .forms import ClientRegistrationForm
from .models import Client

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