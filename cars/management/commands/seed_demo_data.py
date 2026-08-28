from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from cars.models import Car, Expense, FuelRecord, Maintenance, Trip

DEMO_USERNAME = "demo"
DEMO_PASSWORD = "demo12345"


class Command(BaseCommand):
    help = (
        "Creates (or resets) a demo account with a few realistic cars, "
        "trips, fuel-ups and maintenance records so the live deployment "
        "isn't an empty screen. Safe to run more than once."
    )

    def handle(self, *args, **options):
        today = timezone.now().date()

        user, created = User.objects.get_or_create(username=DEMO_USERNAME)
        if created:
            user.set_password(DEMO_PASSWORD)
            user.save()
            self.stdout.write(f"Created user '{DEMO_USERNAME}'.")
        else:
            self.stdout.write(f"User '{DEMO_USERNAME}' already exists, reusing it.")

        camry, camry_new = Car.objects.get_or_create(
            license_plate="DEMO-101",
            defaults=dict(
                owner=user,
                make="toyota",
                model="camry",
                year=2021,
                color="Silver",
                fuel_type="gasoline",
                usage_type="personal",
                current_mileage=34210,
                notes="Daily driver, mostly commuting.",
            ),
        )
        if camry_new:
            self._seed_personal_car(camry, today)

        crv, crv_new = Car.objects.get_or_create(
            license_plate="DEMO-202",
            defaults=dict(
                owner=user,
                make="honda",
                model="cr_v",
                year=2023,
                color="Black",
                fuel_type="gasoline",
                usage_type="taxi",
                current_mileage=51840,
                notes="Runs weekday shifts for a ride-share app.",
            ),
        )
        if crv_new:
            self._seed_taxi_car(crv, today)

        f150, f150_new = Car.objects.get_or_create(
            license_plate="DEMO-303",
            defaults=dict(
                owner=user,
                make="ford",
                model="f_150",
                year=2020,
                color="White",
                fuel_type="gasoline",
                usage_type="fleet",
                fleet_name="Metro Delivery Co.",
                current_mileage=78420,
                notes="Local delivery route, three drivers rotate shifts.",
            ),
        )
        if f150_new:
            self._seed_fleet_car(f150, today)

        self.stdout.write(self.style.SUCCESS(
            f"Demo data ready. Sign in with {DEMO_USERNAME} / {DEMO_PASSWORD}."
        ))

    def _seed_personal_car(self, car, today):
        Maintenance.objects.create(
            car=car,
            service_name="Oil and filter change",
            description="Full synthetic, standard interval.",
            service_date=today - timedelta(days=40),
            cost=79.99,
            mileage_at_service=33800,
            service_provider="Jiffy Lube",
        )
        Expense.objects.create(
            car=car,
            expense_type="insurance",
            description="Monthly auto insurance",
            amount=142.50,
            date=today - timedelta(days=12),
            mileage=34100,
        )
        FuelRecord.objects.create(
            car=car,
            date=today - timedelta(days=6),
            odometer=34210,
            liters=45.00,
            price_per_liter=1.02,
            total_cost=45.90,
            station_name="Shell",
        )

    def _seed_taxi_car(self, car, today):
        Maintenance.objects.create(
            car=car,
            service_name="Brake pads replacement",
            description="Front pads were down to 2mm.",
            service_date=today - timedelta(days=25),
            cost=210.00,
            mileage_at_service=51200,
            service_provider="Midas",
        )
        FuelRecord.objects.create(
            car=car,
            date=today - timedelta(days=3),
            odometer=51840,
            liters=52.30,
            price_per_liter=1.05,
            total_cost=54.92,
            station_name="Costco Gas",
        )
        for days_ago, distance, income in [(9, 62, 118.40), (6, 41, 79.20), (2, 55, 103.75)]:
            start = 51840 - distance * 3
            Trip.objects.create(
                car=car,
                date=today - timedelta(days=days_ago),
                start_mileage=start,
                end_mileage=start + distance,
                income=income,
                trip_type="ride_share",
                passengers=1,
            )

    def _seed_fleet_car(self, car, today):
        Maintenance.objects.create(
            car=car,
            service_name="Tire rotation and alignment",
            service_date=today - timedelta(days=18),
            cost=95.00,
            mileage_at_service=78000,
            service_provider="Discount Tire",
        )
        Expense.objects.create(
            car=car,
            expense_type="registration",
            description="Annual commercial registration renewal",
            amount=310.00,
            date=today - timedelta(days=30),
            mileage=77500,
        )
        FuelRecord.objects.create(
            car=car,
            date=today - timedelta(days=4),
            odometer=78420,
            liters=68.00,
            price_per_liter=1.04,
            total_cost=70.72,
            station_name="Pilot Flying J",
        )
        for days_ago, distance in [(14, 85), (7, 92)]:
            start = 78420 - distance * 2
            Trip.objects.create(
                car=car,
                date=today - timedelta(days=days_ago),
                start_mileage=start,
                end_mileage=start + distance,
                trip_type="delivery",
            )
