from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

User = settings.AUTH_USER_MODEL

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    middle_name = models.CharField(max_length=200)
    phone = PhoneNumberField(blank=False, unique=True)
    car = models.CharField(max_length=200)
    photo = models.ImageField(default='default.jpg', upload_to='driver_pics')
    car_photo = models.ImageField(default=None, upload_to='car_pics')
    passport_photo = models.ImageField(default=None, upload_to='passport_pics')
    insurance_photo = models.ImageField(default=None, upload_to='insurance_pics')
    license_photo = models.ImageField(default=None, upload_to='license_pics')
    description = models.TextField(max_length=1000)
    car_type = models.CharField(max_length=200)
    experience = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    middle_name = models.CharField(max_length=200)
    phone = PhoneNumberField(blank=False, unique=True)

    def __str__(self):
        return str(self.user)

class Order(models.Model):
    address_from = models.CharField(max_length=200)
    address_to = models.CharField(max_length=200)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, default=None, null=True)
    car_type = models.CharField(max_length=200, default='standart')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    price = models.IntegerField()
    prepayment = models.IntegerField(default=0)
    client_payment = models.IntegerField(default=0)
    postpayment = models.IntegerField(default=100)
    distance = models.IntegerField()
    additional_seats = models.IntegerField(default=0)
    additional_poster = models.IntegerField(default=0)
    date_arrive = models.DateTimeField()
    date_start = models.DateTimeField(default=None, null=True)
    date_end = models.DateTimeField(default=None, null=True)
    status = models.CharField(max_length=200)
    client_comment = models.TextField(max_length=1000, default="")
    client_rating = models.IntegerField(default=0)
    driver_rating = models.IntegerField(default=0)

    def __str__(self):
        return self.pk