from django import forms
from .models import Driver, Client, CustomUser
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email",)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email",)

class DriverRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', max_length=30, required=True)
    last_name = forms.CharField(label='Фамилия', max_length=150, required=True)
    middle_name = forms.CharField(label='Отчество', max_length=200, required=True)
    phone = PhoneNumberField(label='Номер телефона', region="RU", required=True)
    car = forms.CharField(label='Название машины', min_length=5, max_length=200, required=True)
    photo = forms.ImageField(label='Ваше фото', required=False)
    car_photo = forms.ImageField(label='Фото машины', required=True)
    passport_photo = forms.ImageField(label='Фото паспорта', required=True)
    insurance_photo = forms.ImageField(label='Фото страхования', required=True)
    license_photo = forms.ImageField(label='Фото лицензии', required=True)
    description = forms.CharField(min_length=100, max_length=1000, widget=forms.Textarea, required=True, label='Описание')
    car_type = forms.CharField(label='Тип машины (стандарт/комфорт/минивэн)', min_length=5,max_length=200, required=True)
    experience = forms.IntegerField(label='Опыт вождения (лет)', min_value=0, required=False)
    email = forms.EmailField(label='Электронная почта', required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['photo', 'first_name', 'last_name', 'middle_name', 'phone', 'email', 'car', 'car_photo',
                  'passport_photo', 'insurance_photo', 'license_photo', 'description', 'car_type', 'experience',
                  'password1', 'password2']

class ClientRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', max_length=30, required=True)
    last_name = forms.CharField(label='Фамилия', max_length=150, required=True)
    middle_name = forms.CharField(max_length=200, required=True, label='Отчество')
    phone = PhoneNumberField(region="RU", required=True, label='Номер телефона')
    photo = forms.ImageField(required=False, label='Ваше фото')
    email = forms.EmailField(required=True, label='Электронная почта')

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['photo', 'first_name', 'last_name', 'middle_name', 'phone', 'email', 'password1', 'password2']