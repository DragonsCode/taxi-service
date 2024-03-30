from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib import messages

from .forms import DriverRegistrationForm
from .models import Driver

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