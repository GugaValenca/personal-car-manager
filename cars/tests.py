from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Car


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

    def test_user_cannot_access_another_users_car_detail(self):
        self.client.login(username="other", password="testpass123")
        response = self.client.get(reverse("cars:car_detail", args=[self.car.pk]))
        self.assertEqual(response.status_code, 404)
