from django.urls import path
from . import views

app_name = 'cars'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cars/', views.car_list, name='car_list'),
    path('cars/<int:pk>/', views.car_detail, name='car_detail'),
    path('maintenances/', views.maintenance_list, name='maintenance_list'),
    path('expenses/', views.expense_list, name='expense_list'),
]
