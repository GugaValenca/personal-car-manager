from django import forms

from .models import Car, Expense, FuelRecord, Trip


class StyledModelForm(forms.ModelForm):
    """Applies Bootstrap-friendly classes to generated fields."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            field.widget.attrs["class"] = css


class CarForm(StyledModelForm):
    class Meta:
        model = Car
        fields = [
            "make",
            "model",
            "year",
            "color",
            "license_plate",
            "fuel_type",
            "usage_type",
            "fleet_name",
            "current_mileage",
            "notes",
            "is_active",
        ]


class ExpenseForm(StyledModelForm):
    class Meta:
        model = Expense
        fields = ["car", "expense_type", "description", "amount", "date", "mileage", "notes"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}


class FuelRecordForm(StyledModelForm):
    class Meta:
        model = FuelRecord
        fields = [
            "car",
            "date",
            "odometer",
            "liters",
            "price_per_liter",
            "total_cost",
            "full_tank",
            "station_name",
            "notes",
        ]
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}


class TripForm(StyledModelForm):
    class Meta:
        model = Trip
        fields = [
            "car",
            "date",
            "start_mileage",
            "end_mileage",
            "income",
            "trip_type",
            "passengers",
            "notes",
        ]
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}
