from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from .models import Car, Maintenance, Expense


def home(request):
    """Homepage - accessible to everyone"""
    return render(request, 'cars/home.html')


@login_required
def dashboard(request):
    """Dashboard with user's car statistics"""
    user_cars = Car.objects.filter(owner=request.user)

    # Statistics
    total_cars = user_cars.count()
    total_maintenances = Maintenance.objects.filter(
        car__owner=request.user).count()
    total_expenses = Expense.objects.filter(car__owner=request.user).aggregate(
        total=Sum('amount')
    )['total'] or 0

    # Recent activities
    recent_maintenances = Maintenance.objects.filter(
        car__owner=request.user)[:5]
    recent_expenses = Expense.objects.filter(car__owner=request.user)[:5]

    context = {
        'total_cars': total_cars,
        'total_maintenances': total_maintenances,
        'total_expenses': total_expenses,
        'user_cars': user_cars,
        'recent_maintenances': recent_maintenances,
        'recent_expenses': recent_expenses,
    }
    return render(request, 'cars/dashboard.html', context)


@login_required
def car_list(request):
    """List all user's cars"""
    cars = Car.objects.filter(owner=request.user)
    return render(request, 'cars/car_list.html', {'cars': cars})


@login_required
def car_detail(request, pk):
    """Detail view of a specific car"""
    car = get_object_or_404(Car, pk=pk, owner=request.user)
    maintenances = car.maintenances.all()[:10]
    expenses = car.expenses.all()[:10]

    # Car statistics
    total_maintenance_cost = car.maintenances.aggregate(
        total=Sum('cost')
    )['total'] or 0

    total_expense_cost = car.expenses.aggregate(
        total=Sum('amount')
    )['total'] or 0

    context = {
        'car': car,
        'maintenances': maintenances,
        'expenses': expenses,
        'total_maintenance_cost': total_maintenance_cost,
        'total_expense_cost': total_expense_cost,
        'total_cost': total_maintenance_cost + total_expense_cost,
    }
    return render(request, 'cars/car_detail.html', context)


@login_required
def maintenance_list(request):
    """List all user's maintenances"""
    maintenances = Maintenance.objects.filter(car__owner=request.user)
    return render(request, 'cars/maintenance_list.html', {'maintenances': maintenances})


@login_required
def expense_list(request):
    """List all user's expenses"""
    expenses = Expense.objects.filter(car__owner=request.user)
    return render(request, 'cars/expense_list.html', {'expenses': expenses})
