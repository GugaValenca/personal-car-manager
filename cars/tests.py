from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Car, Expense, FuelRecord, Maintenance, Trip


class CarViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="owner", password="testpass123")
        self.other_user = User.objects.create_user(
            username="other", password="testpass123"
        )
        self.car = Car.objects.create(
            owner=self.user,
            make="honda",
            model="civic",
            year=2020,
            color="Blue",
            license_plate="ABC-1234",
            fuel_type="gasoline",
            current_mileage=45000,
        )

    def test_logged_user_can_access_car_pages(self):
        self.client.login(username="owner", password="testpass123")

        response = self.client.get(reverse("cars:car_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ABC-1234")

        response = self.client.get(reverse("cars:car_detail", args=[self.car.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "2020")

        response = self.client.get(reverse("cars:maintenance_list"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("cars:expense_list"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("cars:fuel_list"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("cars:trip_list"))
        self.assertEqual(response.status_code, 200)

    def test_user_cannot_access_another_users_car_detail(self):
        self.client.login(username="other", password="testpass123")
        response = self.client.get(reverse("cars:car_detail", args=[self.car.pk]))
        self.assertEqual(response.status_code, 404)

    def test_dashboard_api_returns_user_summary(self):
        Maintenance.objects.create(
            car=self.car,
            service_name="Oil Change",
            service_date="2026-03-01",
            cost="120.00",
            mileage_at_service=45100,
        )
        Expense.objects.create(
            car=self.car,
            expense_type="insurance",
            description="Monthly insurance",
            amount="90.00",
            date="2026-03-01",
        )
        FuelRecord.objects.create(
            car=self.car,
            date="2026-03-01",
            odometer=45200,
            liters="40.00",
            price_per_liter="1.40",
            total_cost="56.00",
        )
        Trip.objects.create(
            car=self.car,
            date="2026-03-01",
            start_mileage=45200,
            end_mileage=45300,
            income="180.00",
            trip_type="taxi",
        )

        self.client.login(username="owner", password="testpass123")
        response = self.client.get(reverse("cars:dashboard_api"))
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["summary"]["total_cars"], 1)
        self.assertEqual(payload["summary"]["total_trip_distance"], 100)
        self.assertEqual(payload["summary"]["total_trip_income"], 180.0)
