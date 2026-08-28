from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
import json
import re

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
        self.client.force_login(self.user)

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
        self.client.force_login(self.other_user)
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

        self.client.force_login(self.user)
        response = self.client.get(reverse("cars:dashboard_api"))
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["summary"]["total_cars"], 1)
        self.assertEqual(payload["summary"]["total_trip_distance"], 100)
        self.assertEqual(payload["summary"]["total_trip_income"], 180.0)

    def test_user_can_create_car_via_ui_form(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("cars:car_create"),
            {
                "make": "toyota",
                "model": "corolla",
                "year": 2022,
                "color": "White",
                "license_plate": "NEW-2022",
                "fuel_type": "gasoline",
                "usage_type": "personal",
                "fleet_name": "",
                "current_mileage": 12000,
                "notes": "Created via UI form",
                "is_active": "on",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Car.objects.filter(owner=self.user, license_plate="NEW-2022").exists())

    def test_frontend_login_endpoint_authenticates_user(self):
        response = self.client.post(
            reverse("cars:frontend_login"),
            data=json.dumps({"username": "owner", "password": "testpass123"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload["ok"])

    def test_signup_page_creates_user(self):
        response = self.client.post(
            reverse("cars:signup"),
            {
                "username": "new_user",
                "password1": "StrongPass12345",
                "password2": "StrongPass12345",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="new_user").exists())

    def test_license_plate_must_be_unique(self):
        """Regression test for the missing `unique=True` on Car.license_plate."""
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("cars:car_create"),
            {
                "make": "toyota",
                "model": "corolla",
                "year": 2022,
                "color": "White",
                "license_plate": "ABC-1234",  # already used by self.car
                "fuel_type": "gasoline",
                "usage_type": "personal",
                "fleet_name": "",
                "current_mileage": 12000,
                "notes": "",
                "is_active": "on",
            },
        )
        self.assertEqual(response.status_code, 200)  # re-renders form with errors
        self.assertFormError(response.context["form"], "license_plate", "Car with this License Plate already exists.")
        self.assertEqual(Car.objects.filter(license_plate="ABC-1234").count(), 1)

    def test_user_can_create_maintenance_via_ui_form(self):
        """Regression test: Maintenance previously had no non-admin create flow."""
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("cars:maintenance_create"),
            {
                "car": self.car.pk,
                "service_name": "Oil Change",
                "description": "Full synthetic oil change",
                "service_date": "2026-03-01",
                "cost": "89.90",
                "mileage_at_service": 45300,
                "service_provider": "Quick Lube",
                "notes": "",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Maintenance.objects.filter(car=self.car, service_name="Oil Change").exists()
        )
        self.car.refresh_from_db()
        self.assertEqual(self.car.current_mileage, 45300)

    def test_maintenance_create_only_lists_own_active_cars(self):
        other_car = Car.objects.create(
            owner=self.other_user,
            make="ford",
            model="focus",
            year=2019,
            color="Red",
            license_plate="OTH-9999",
            fuel_type="gasoline",
            current_mileage=1000,
        )
        self.client.force_login(self.user)
        response = self.client.get(reverse("cars:maintenance_create"))
        car_choices = list(response.context["form"].fields["car"].queryset)
        self.assertIn(self.car, car_choices)
        self.assertNotIn(other_car, car_choices)

    def test_car_list_is_paginated(self):
        """Regression test for unbounded list views (no pagination)."""
        for i in range(25):
            Car.objects.create(
                owner=self.user,
                make="toyota",
                model="corolla",
                year=2000 + i,
                color="Gray",
                license_plate=f"PAG-{i:04d}",
                fuel_type="gasoline",
                current_mileage=1000,
            )

        self.client.force_login(self.user)
        response = self.client.get(reverse("cars:car_list"))
        page = response.context["cars"]
        self.assertEqual(page.paginator.count, 26)  # 25 created here + self.car
        self.assertEqual(len(page.object_list), 20)  # PAGE_SIZE

        response = self.client.get(reverse("cars:car_list") + "?page=2")
        page = response.context["cars"]
        self.assertEqual(len(page.object_list), 6)

    def test_static_theme_css_is_served(self):
        """Regression test: /static/ had no URL route and 404'd (confirmed live)."""
        response = self.client.get("/static/css/theme.css")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/css", response.headers["Content-Type"])

    def test_static_route_also_serves_django_admins_own_assets(self):
        """Regression guard: a route that only serves our STATICFILES_DIRS
        (and not installed apps' static/, e.g. django.contrib.admin) would
        fix theme.css/favicon while silently leaving the actual admin UI
        (list/add/change pages, not just the custom login screen) unstyled."""
        response = self.client.get("/static/admin/css/base.css")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/css", response.headers["Content-Type"])

    def test_home_page_references_an_existing_built_asset(self):
        """Regression test: templates used to hardcode Vite's hashed filenames,
        which went stale (404) the moment someone ran `npm run build` again.
        The page must reference whatever the manifest currently points to,
        and that file must actually exist and be servable."""
        response = self.client.get(reverse("cars:home"))
        self.assertEqual(response.status_code, 200)

        js_match = re.search(r'src="(/assets/index-[^"]+\.js)"', response.content.decode())
        css_match = re.search(r'href="(/assets/index-[^"]+\.css)"', response.content.decode())
        self.assertIsNotNone(js_match, "home page did not render a JS bundle URL")
        self.assertIsNotNone(css_match, "home page did not render a CSS bundle URL")

        for asset_url in (js_match.group(1), css_match.group(1)):
            asset_response = self.client.get(asset_url)
            self.assertEqual(asset_response.status_code, 200, f"{asset_url} is not servable")


class FrontendLoginCsrfTests(TestCase):
    """frontend_login used to be @csrf_exempt (login CSRF risk). These tests
    run with CSRF checks enforced, unlike the default test Client."""

    def setUp(self):
        self.user = User.objects.create_user(username="owner", password="testpass123")
        self.client = Client(enforce_csrf_checks=True)

    def test_login_without_csrf_token_is_rejected(self):
        # Visiting home() sets the csrftoken cookie (ensure_csrf_cookie) but we
        # deliberately don't send it back, simulating a cross-site POST.
        self.client.get(reverse("cars:home"))
        response = self.client.post(
            reverse("cars:frontend_login"),
            data=json.dumps({"username": "owner", "password": "testpass123"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

    def test_login_with_csrf_token_succeeds(self):
        self.client.get(reverse("cars:home"))
        csrf_token = self.client.cookies["csrftoken"].value
        response = self.client.post(
            reverse("cars:frontend_login"),
            data=json.dumps({"username": "owner", "password": "testpass123"}),
            content_type="application/json",
            HTTP_X_CSRFTOKEN=csrf_token,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["ok"])


class LoginLockoutTests(TestCase):
    """Neither /auth/login/ nor /admin/login/ had any brute-force protection.
    django-axes hooks into authenticate() via AUTHENTICATION_BACKENDS, so a
    single settings change covers both without touching either view."""

    def setUp(self):
        self.user = User.objects.create_user(username="owner", password="testpass123")

    def test_repeated_failed_logins_get_locked_out(self):
        # AXES_FAILURE_LIMIT = 5: the first 4 wrong attempts are ordinary
        # rejections, the 5th is where axes actually applies the lockout.
        statuses = []
        for _ in range(5):
            response = self.client.post(
                reverse("cars:frontend_login"),
                data=json.dumps({"username": "owner", "password": "wrong-password"}),
                content_type="application/json",
            )
            statuses.append(response.status_code)
        self.assertEqual(statuses, [401, 401, 401, 401, 429])

        # Locked out means locked out - the right password doesn't help anymore.
        response = self.client.post(
            reverse("cars:frontend_login"),
            data=json.dumps({"username": "owner", "password": "testpass123"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 429)
