from django.contrib import admin
from .models import Car, Maintenance, Expense, FuelRecord, Trip


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'owner', 'usage_type', 'license_plate',
                    'fuel_type', 'current_mileage', 'is_active', 'created_at']
    list_filter = ['make', 'fuel_type', 'usage_type', 'is_active', 'year', 'created_at']
    search_fields = ['make', 'model', 'license_plate', 'owner__username']
    readonly_fields = ['created_at']

    fieldsets = (
        ('Vehicle Information', {
            'fields': (
                'owner',
                'make',
                'model',
                'year',
                'color',
                'fuel_type',
                'usage_type',
                'fleet_name',
                'is_active',
            )
        }),
        ('Registration Details', {
            'fields': ('license_plate', 'current_mileage')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('System Information', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(FuelRecord)
class FuelRecordAdmin(admin.ModelAdmin):
    list_display = ["car", "date", "liters", "price_per_liter", "total_cost", "odometer"]
    list_filter = ["date", "car__usage_type", "car__make"]
    search_fields = ["car__license_plate", "car__owner__username", "station_name"]
    readonly_fields = ["created_at"]
    date_hierarchy = "date"


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ["car", "date", "trip_type", "distance_km", "income", "passengers"]
    list_filter = ["date", "trip_type", "car__usage_type", "car__make"]
    search_fields = ["car__license_plate", "car__owner__username", "notes"]
    readonly_fields = ["distance_km", "created_at"]
    date_hierarchy = "date"


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ['car', 'service_name',
                    'service_date', 'cost', 'service_provider']
    list_filter = ['service_date', 'car__make', 'car__model']
    search_fields = ['service_name', 'car__make',
                     'car__model', 'service_provider']
    readonly_fields = ['created_at']
    date_hierarchy = 'service_date'

    fieldsets = (
        ('Service Information', {
            'fields': ('car', 'service_name', 'description')
        }),
        ('Service Details', {
            'fields': ('service_date', 'mileage_at_service', 'cost', 'service_provider')
        }),
        ('Additional Notes', {
            'fields': ('notes',)
        }),
        ('System Information', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['car', 'description', 'amount', 'expense_type', 'date']
    list_filter = ['expense_type', 'date', 'car__make']
    search_fields = ['description', 'car__make', 'car__model']
    readonly_fields = ['created_at']
    date_hierarchy = 'date'

    fieldsets = (
        ('Expense Information', {
            'fields': ('car', 'expense_type', 'description')
        }),
        ('Financial Details', {
            'fields': ('amount', 'date', 'mileage')
        }),
        ('Additional Notes', {
            'fields': ('notes',)
        }),
        ('System Information', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
