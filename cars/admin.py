from django.contrib import admin
from .models import Car, Maintenance, Expense


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'owner', 'license_plate',
                    'fuel_type', 'current_mileage', 'created_at']
    list_filter = ['make', 'fuel_type', 'year', 'created_at']
    search_fields = ['make', 'model', 'license_plate', 'owner__username']
    readonly_fields = ['created_at']

    fieldsets = (
        ('Vehicle Information', {
            'fields': ('owner', 'make', 'model', 'year', 'color', 'fuel_type')
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
