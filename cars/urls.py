from django.urls import path
from . import views

app_name = 'cars'

urlpatterns = [
    path("assets/<path:filename>", views.frontend_asset, name="frontend_asset"),
    path("auth/login/", views.frontend_login, name="frontend_login"),
    path("signup/", views.signup, name="signup"),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("api/dashboard/", views.dashboard_api, name="dashboard_api"),
    path('cars/', views.car_list, name='car_list'),
    path("cars/new/", views.car_create, name="car_create"),
    path('cars/<int:pk>/', views.car_detail, name='car_detail'),
    path('maintenances/', views.maintenance_list, name='maintenance_list'),
    path('expenses/', views.expense_list, name='expense_list'),
    path("expenses/new/", views.expense_create, name="expense_create"),
    path("fuel-records/", views.fuel_list, name="fuel_list"),
    path("fuel-records/new/", views.fuel_create, name="fuel_create"),
    path("trips/", views.trip_list, name="trip_list"),
    path("trips/new/", views.trip_create, name="trip_create"),
]
