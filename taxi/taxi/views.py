from django.http import HttpResponse, JsonResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from django.views.generic.edit import CreateView, UpdateView, DeleteView # for future use

from django.shortcuts import render, redirect

from osmapi import OsmApi

from .models import Driver, Client, Order
from .forms import NewOrderForm, NewUserOrderForm
from .map_funcs import calculate_distance, decode_polyline, pos, calculate_order

import requests
import folium


def request_order(request):
    if request.method == 'POST':
        # Use NewUserOrderForm for both authenticated and unauthenticated users
        if not request.user.is_authenticated:
            form = NewUserOrderForm(request.POST)

            if form.is_valid():
                # Create a new User instance (assuming email is the username)
                user = User.objects.create_user(
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password1']
                )
                # Create a new Client instance associated with the User
                client = Client.objects.create(user=user)

                # Populate remaining Client fields and Order data
                client.first_name = form.cleaned_data['first_name']
                client.last_name = form.cleaned_data['last_name']
                client.middle_name = form.cleaned_data['middle_name']
                client.phone = form.cleaned_data['phone']
                client.save()
            else:
                return render(request, 'taxi/request_order.html', {'form': form})
        else:
            client = Client.objects.get(user=request.user)
            form = NewOrderForm(request.POST)
            if not form.is_valid():
                return render(request, 'taxi/request_order.html', {'form': form})

        price, distance = calculate_order(form.cleaned_data['address_from'], form.cleaned_data['address_to'], form.cleaned_data['car_type'])

        # Order data (assuming price is calculated elsewhere)
        order = Order(
            address_from=form.cleaned_data['address_from'],
            address_to=form.cleaned_data['address_to'],
            car_type=form.cleaned_data['car_type'],
            date_arrive=form.cleaned_data['date_arrive'],
            additional_seats=form.cleaned_data['additional_seats'],
            additional_poster=form.cleaned_data['additional_poster'],
            price=price,
            client=client,  # Associate with the newly created client
            distance=distance,
            status='Новый',
            # ... other order fields (driver, status, etc.)
        )

        order.save()

        # Handle successful order creation (e.g., redirect to confirmation page)
        return redirect('profile')
    else:
        if not request.user.is_authenticated:
            form = NewUserOrderForm()
            return render(request, 'taxi/request_order.html', {'form': form})
        
        User = get_user_model()
        user = User.objects.get(email=request.user)
        if not user:
            messages.error(request, 'Пользователь не найден')
            return redirect('login')
        client = Client.objects.get(user=user)
        if not client:
            messages.error(request, 'Клиент не найден')
            return redirect('client_register')
        
        form = NewOrderForm()

        return render(request, 'taxi/request_order.html', {'form': form})

def calculate_price(request):
    # Access request parameters (assuming they are named pick_up_address, drop_off_address, and car_type)
    pick_up_address = request.GET.get('pick_up_address')
    drop_off_address = request.GET.get('drop_off_address')
    car_type = request.GET.get('car_type')
    try:
        calculated_price, distance_km = calculate_order(pick_up_address, drop_off_address, car_type)
    except Exception as e:
        return JsonResponse({'error': str(e)})
    return JsonResponse({'price': calculated_price, 'distance': distance_km})


def show_route(request):
    point1_lat = request.GET.get('point1_lat')
    point1_lon = request.GET.get('point1_lon')
    point2_lat = request.GET.get('point2_lat')
    point2_lon = request.GET.get('point2_lon')

    # Запрос к OSRM API для получения маршрута для автомобиля
    osrm_url = f'http://router.project-osrm.org/route/v1/driving/{point1_lon},{point1_lat};{point2_lon},{point2_lat}?overview=full&steps=true'
    response = requests.get(osrm_url)
    route_data = response.json()

    # Создание карты с помощью folium
    my_map = folium.Map(location=[point1_lat, point1_lon], zoom_start=12)

    # Добавление маршрута на карту
    route_coordinates = []
    for leg in route_data['routes'][0]['legs']:
        for step in leg['steps']:
            geometry = step['geometry']
            coordinates = decode_polyline(geometry)
            route_coordinates.extend(coordinates)
    folium.PolyLine(locations=route_coordinates, color='blue').add_to(my_map)

    # Вычисление длины маршрута
    distance_km = calculate_distance(route_coordinates)

    # Добавление маркеров для точек
    folium.Marker([point1_lat, point1_lon], popup=f'Точка 1. Расстояние: {distance_km:.2f} км').add_to(my_map)
    folium.Marker([point2_lat, point2_lon], popup=f'Точка 2. Расстояние: {distance_km:.2f} км').add_to(my_map)

    # Получение HTML-кода карты
    map_html = my_map.get_root().render()

    # Возвращение HTML-кода карты как HTTP-ответ
    return HttpResponse(map_html)


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