from django import forms
from .models import Driver, Client, CustomUser
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils import timezone

from datetime import datetime, timedelta


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
    email = forms.EmailField(required=True, label='Электронная почта')

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['first_name', 'last_name', 'middle_name', 'phone', 'email', 'password1', 'password2']

class NewOrderForm(forms.Form):
    address_from = forms.CharField(label='Адрес откуда', max_length=200, required=True, widget=forms.TextInput(attrs={'id': 'pick_up_address'}))
    address_to = forms.CharField(label='Адрес куда', max_length=200, required=True, widget=forms.TextInput(attrs={'id': 'drop_off_address'}))
    car_type = forms.ChoiceField(label='Тип машины', choices=[('standard', 'Стандарт'), ('comfort', 'Комфорт'), ('minivan', 'Минивэн')], required=True, widget=forms.Select(attrs={'id': 'car_type'}))
    date_arrive = forms.DateTimeField(label='Дата прибытия', initial=datetime.now() + timedelta(hours=1), required=True, widget=forms.DateTimeInput(attrs={'id': 'date_arrive_field', 'type': 'datetime-local'}))
    additional_seats = forms.IntegerField(label='Дополнительные места', min_value=0, initial=0, required=False)
    additional_poster = forms.IntegerField(label='Дополнительный постер', min_value=0, initial=0, required=False)
    price = forms.IntegerField(label='Стоимость', min_value=0, initial=0, disabled=True, widget=forms.NumberInput(attrs={'id': 'price_field'}))
    distance = forms.IntegerField(label='Расстояние', min_value=0, initial=0, disabled=True, widget=forms.NumberInput(attrs={'id': 'distance_field'}))

    def clean_date_arrive(self):
        date_arrive = self.cleaned_data['date_arrive']
        if date_arrive < timezone.now():
            raise forms.ValidationError("Дата прибытия не может быть в прошлом.")
        return date_arrive

class NewUserOrderForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', max_length=30, required=True)
    last_name = forms.CharField(label='Фамилия', max_length=150, required=True)
    middle_name = forms.CharField(max_length=200, required=True, label='Отчество')
    phone = PhoneNumberField(region="RU", required=True, label='Номер телефона')
    email = forms.EmailField(required=True, label='Электронная почта')

    address_from = forms.CharField(label='Адрес откуда', max_length=200, required=True, widget=forms.TextInput(attrs={'id': 'pick_up_address'}))
    address_to = forms.CharField(label='Адрес куда', max_length=200, required=True, widget=forms.TextInput(attrs={'id': 'drop_off_address'}))
    car_type = forms.ChoiceField(label='Тип машины', choices=[('standard', 'Стандарт'), ('comfort', 'Комфорт'), ('minivan', 'Минивэн')], required=True, widget=forms.Select(attrs={'id': 'car_type'}))
    date_arrive = forms.DateTimeField(label='Дата прибытия', initial=datetime.now() + timedelta(hours=1), required=True, widget=forms.DateTimeInput(attrs={'id': 'date_arrive_field', 'type': 'datetime-local'}))
    additional_seats = forms.IntegerField(label='Дополнительные места', min_value=0, max_value=2, initial=0, required=False)
    additional_poster = forms.IntegerField(label='Дополнительный постер', min_value=0, max_value=5, initial=0, required=False)
    price = forms.IntegerField(label='Стоимость', min_value=0, initial=0, disabled=True, widget=forms.NumberInput(attrs={'id': 'price_field'}))
    distance = forms.IntegerField(label='Расстояние', min_value=0, initial=0, disabled=True, widget=forms.NumberInput(attrs={'id': 'distance_field'}))

    def clean_date_arrive(self):
        date_arrive = self.cleaned_data['date_arrive']
        if date_arrive < timezone.now():
            raise forms.ValidationError("Дата прибытия не может быть в прошлом.")
        return date_arrive
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['first_name', 'last_name', 'middle_name', 'phone', 'email', 'password1', 'password2']