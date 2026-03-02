from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Car, Maintenance, Expense, FuelRecord, Trip
from .forms import CarForm, ExpenseForm, FuelRecordForm, TripForm


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
    total_maintenance_cost = Maintenance.objects.filter(car__owner=request.user).aggregate(
        total=Sum("cost")
    )["total"] or 0
    total_fuel_cost = FuelRecord.objects.filter(car__owner=request.user).aggregate(
        total=Sum("total_cost")
    )["total"] or 0
    total_trip_income = Trip.objects.filter(car__owner=request.user).aggregate(
        total=Sum("income")
    )["total"] or 0
    total_trip_distance = Trip.objects.filter(car__owner=request.user).aggregate(
        total=Sum("distance_km")
    )["total"] or 0
    net_balance = total_trip_income - (
        total_expenses + total_maintenance_cost + total_fuel_cost
    )

    # Recent activities
    recent_maintenances = Maintenance.objects.filter(
        car__owner=request.user)[:5]
    recent_expenses = Expense.objects.filter(car__owner=request.user)[:5]
    recent_fuel_records = FuelRecord.objects.filter(car__owner=request.user)[:5]
    recent_trips = Trip.objects.filter(car__owner=request.user)[:5]

    context = {
        'total_cars': total_cars,
        'total_maintenances': total_maintenances,
        'total_expenses': total_expenses,
        "total_maintenance_cost": total_maintenance_cost,
        "total_fuel_cost": total_fuel_cost,
        "total_trip_income": total_trip_income,
        "total_trip_distance": total_trip_distance,
        "net_balance": net_balance,
        'user_cars': user_cars,
        'recent_maintenances': recent_maintenances,
        'recent_expenses': recent_expenses,
        "recent_fuel_records": recent_fuel_records,
        "recent_trips": recent_trips,
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


@login_required
def fuel_list(request):
    """List all user's fuel records"""
    fuel_records = FuelRecord.objects.filter(car__owner=request.user)
    return render(request, "cars/fuel_list.html", {"fuel_records": fuel_records})


@login_required
def trip_list(request):
    """List all user's trips"""
    trips = Trip.objects.filter(car__owner=request.user)
    return render(request, "cars/trip_list.html", {"trips": trips})


@login_required
def dashboard_api(request):
    """JSON endpoint for frontend integration"""
    user_cars = Car.objects.filter(owner=request.user)
    total_expenses = Expense.objects.filter(car__owner=request.user).aggregate(
        total=Sum("amount")
    )["total"] or 0
    total_maintenance_cost = Maintenance.objects.filter(car__owner=request.user).aggregate(
        total=Sum("cost")
    )["total"] or 0
    total_fuel_cost = FuelRecord.objects.filter(car__owner=request.user).aggregate(
        total=Sum("total_cost")
    )["total"] or 0
    total_trip_income = Trip.objects.filter(car__owner=request.user).aggregate(
        total=Sum("income")
    )["total"] or 0
    total_trip_distance = Trip.objects.filter(car__owner=request.user).aggregate(
        total=Sum("distance_km")
    )["total"] or 0

    data = {
        "summary": {
            "total_cars": user_cars.count(),
            "total_expenses": float(total_expenses),
            "total_maintenance_cost": float(total_maintenance_cost),
            "total_fuel_cost": float(total_fuel_cost),
            "total_trip_income": float(total_trip_income),
            "total_trip_distance": int(total_trip_distance),
            "net_balance": float(
                total_trip_income - (total_expenses + total_maintenance_cost + total_fuel_cost)
            ),
        },
        "cars": [
            {
                "id": car.id,
                "label": str(car),
                "usage_type": car.usage_type,
                "fleet_name": car.fleet_name,
                "current_mileage": car.current_mileage,
                "is_active": car.is_active,
            }
            for car in user_cars[:10]
        ],
        "recent_expenses": [
            {
                "car": str(expense.car),
                "description": expense.description,
                "amount": float(expense.amount),
                "date": expense.date.isoformat(),
                "type": expense.expense_type,
            }
            for expense in Expense.objects.filter(car__owner=request.user)[:10]
        ],
        "recent_trips": [
            {
                "car": str(trip.car),
                "trip_type": trip.trip_type,
                "distance_km": trip.distance_km,
                "income": float(trip.income),
                "date": trip.date.isoformat(),
            }
            for trip in Trip.objects.filter(car__owner=request.user)[:10]
        ],
    }
    return JsonResponse(data)


def _limit_car_queryset_to_owner(form, user):
    if "car" in form.fields:
        form.fields["car"].queryset = Car.objects.filter(owner=user, is_active=True)


def _sync_car_mileage(car, mileage):
    if mileage and mileage > car.current_mileage:
        car.current_mileage = mileage
        car.save(update_fields=["current_mileage"])


@login_required
def car_create(request):
    if request.method == "POST":
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            messages.success(request, "Car created successfully.")
            return redirect("cars:car_list")
    else:
        form = CarForm()
    return render(
        request,
        "cars/form_page.html",
        {"form": form, "title": "Add Car", "subtitle": "Register a vehicle in your account."},
    )


@login_required
def expense_create(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        _limit_car_queryset_to_owner(form, request.user)
        if form.is_valid():
            expense = form.save()
            _sync_car_mileage(expense.car, expense.mileage)
            messages.success(request, "Expense created successfully.")
            return redirect("cars:expense_list")
    else:
        form = ExpenseForm()
        _limit_car_queryset_to_owner(form, request.user)
    return render(
        request,
        "cars/form_page.html",
        {
            "form": form,
            "title": "Add Expense",
            "subtitle": "Track costs like insurance, parking, and maintenance bills.",
        },
    )


@login_required
def fuel_create(request):
    if request.method == "POST":
        form = FuelRecordForm(request.POST)
        _limit_car_queryset_to_owner(form, request.user)
        if form.is_valid():
            fuel = form.save()
            _sync_car_mileage(fuel.car, fuel.odometer)
            messages.success(request, "Fuel record created successfully.")
            return redirect("cars:fuel_list")
    else:
        form = FuelRecordForm()
        _limit_car_queryset_to_owner(form, request.user)
    return render(
        request,
        "cars/form_page.html",
        {
            "form": form,
            "title": "Add Fuel Record",
            "subtitle": "Register fuel volume, cost and odometer for efficiency control.",
        },
    )


@login_required
def trip_create(request):
    if request.method == "POST":
        form = TripForm(request.POST)
        _limit_car_queryset_to_owner(form, request.user)
        if form.is_valid():
            trip = form.save()
            _sync_car_mileage(trip.car, trip.end_mileage)
            messages.success(request, "Trip created successfully.")
            return redirect("cars:trip_list")
    else:
        form = TripForm()
        _limit_car_queryset_to_owner(form, request.user)
    return render(
        request,
        "cars/form_page.html",
        {
            "form": form,
            "title": "Add Trip",
            "subtitle": "Record trip distance and income for taxi/fleet profitability.",
        },
    )
