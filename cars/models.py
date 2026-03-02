from django.db import models
from django.contrib.auth.models import User


class Car(models.Model):
    FUEL_CHOICES = [
        ('gasoline', 'Gasoline'),
        ('diesel', 'Diesel'),
        ('hybrid', 'Hybrid'),
        ('electric', 'Electric'),
    ]
    USAGE_CHOICES = [
        ("personal", "Personal"),
        ("taxi", "Taxi"),
        ("fleet", "Fleet"),
        ("delivery", "Delivery"),
        ("other", "Other"),
    ]

    # Principais marcas do mercado americano
    MAKE_CHOICES = [
        ('ford', 'Ford'),
        ('chevrolet', 'Chevrolet'),
        ('dodge', 'Dodge'),
        ('jeep', 'Jeep'),
        ('ram', 'Ram'),
        ('cadillac', 'Cadillac'),
        ('buick', 'Buick'),
        ('gmc', 'GMC'),
        ('lincoln', 'Lincoln'),
        ('chrysler', 'Chrysler'),
        ('tesla', 'Tesla'),
        ('toyota', 'Toyota'),
        ('honda', 'Honda'),
        ('nissan', 'Nissan'),
        ('hyundai', 'Hyundai'),
        ('kia', 'Kia'),
        ('mazda', 'Mazda'),
        ('subaru', 'Subaru'),
        ('volkswagen', 'Volkswagen'),
        ('bmw', 'BMW'),
        ('mercedes', 'Mercedes-Benz'),
        ('audi', 'Audi'),
        ('lexus', 'Lexus'),
        ('acura', 'Acura'),
        ('infiniti', 'Infiniti'),
        ('volvo', 'Volvo'),
        ('jaguar', 'Jaguar'),
        ('land_rover', 'Land Rover'),
        ('porsche', 'Porsche'),
        ('maserati', 'Maserati'),
        ('other', 'Other'),
    ]

    # Modelos populares por categoria
    MODEL_CHOICES = [
        # Ford Models
        ('f_150', 'F-150'),
        ('mustang', 'Mustang'),
        ('explorer', 'Explorer'),
        ('escape', 'Escape'),
        ('fusion', 'Fusion'),
        ('focus', 'Focus'),
        ('edge', 'Edge'),
        ('expedition', 'Expedition'),
        ('ranger', 'Ranger'),
        ('bronco', 'Bronco'),

        # Chevrolet Models
        ('silverado', 'Silverado'),
        ('equinox', 'Equinox'),
        ('malibu', 'Malibu'),
        ('tahoe', 'Tahoe'),
        ('suburban', 'Suburban'),
        ('camaro', 'Camaro'),
        ('corvette', 'Corvette'),
        ('traverse', 'Traverse'),
        ('cruze', 'Cruze'),
        ('impala', 'Impala'),

        # Toyota Models
        ('camry', 'Camry'),
        ('corolla', 'Corolla'),
        ('rav4', 'RAV4'),
        ('highlander', 'Highlander'),
        ('prius', 'Prius'),
        ('tacoma', 'Tacoma'),
        ('tundra', 'Tundra'),
        ('sienna', 'Sienna'),
        ('avalon', 'Avalon'),
        ('4runner', '4Runner'),

        # Honda Models
        ('civic', 'Civic'),
        ('accord', 'Accord'),
        ('cr_v', 'CR-V'),
        ('pilot', 'Pilot'),
        ('odyssey', 'Odyssey'),
        ('ridgeline', 'Ridgeline'),
        ('hr_v', 'HR-V'),
        ('passport', 'Passport'),
        ('fit', 'Fit'),
        ('insight', 'Insight'),

        # Nissan Models
        ('altima', 'Altima'),
        ('sentra', 'Sentra'),
        ('rogue', 'Rogue'),
        ('murano', 'Murano'),
        ('pathfinder', 'Pathfinder'),
        ('frontier', 'Frontier'),
        ('titan', 'Titan'),
        ('maxima', 'Maxima'),
        ('versa', 'Versa'),
        ('armada', 'Armada'),

        # Tesla Models
        ('model_s', 'Model S'),
        ('model_3', 'Model 3'),
        ('model_x', 'Model X'),
        ('model_y', 'Model Y'),
        ('cybertruck', 'Cybertruck'),

        # BMW Models
        ('3_series', '3 Series'),
        ('5_series', '5 Series'),
        ('7_series', '7 Series'),
        ('x3', 'X3'),
        ('x5', 'X5'),
        ('x7', 'X7'),
        ('i4', 'i4'),
        ('ix', 'iX'),

        # Mercedes Models
        ('c_class', 'C-Class'),
        ('e_class', 'E-Class'),
        ('s_class', 'S-Class'),
        ('glc', 'GLC'),
        ('gle', 'GLE'),
        ('gls', 'GLS'),
        ('eqc', 'EQC'),
        ('g_class', 'G-Class'),

        # Dodge Models
        ('challenger', 'Challenger'),
        ('charger', 'Charger'),
        ('durango', 'Durango'),
        ('journey', 'Journey'),

        # Jeep Models
        ('wrangler', 'Wrangler'),
        ('grand_cherokee', 'Grand Cherokee'),
        ('cherokee', 'Cherokee'),
        ('compass', 'Compass'),
        ('renegade', 'Renegade'),
        ('gladiator', 'Gladiator'),

        # Hyundai Models
        ('elantra', 'Elantra'),
        ('sonata', 'Sonata'),
        ('tucson', 'Tucson'),
        ('santa_fe', 'Santa Fe'),
        ('palisade', 'Palisade'),
        ('kona', 'Kona'),
        ('ioniq', 'Ioniq'),

        # Outros
        ('other', 'Other'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    make = models.CharField(
        max_length=50, choices=MAKE_CHOICES, verbose_name="Make")
    model = models.CharField(
        max_length=50, choices=MODEL_CHOICES, verbose_name="Model")
    year = models.IntegerField(verbose_name="Year")
    color = models.CharField(max_length=30, verbose_name="Color")
    license_plate = models.CharField(
        max_length=20, verbose_name="License Plate")
    fuel_type = models.CharField(
        max_length=20, choices=FUEL_CHOICES, verbose_name="Fuel Type")
    usage_type = models.CharField(
        max_length=20,
        choices=USAGE_CHOICES,
        default="personal",
        verbose_name="Usage Type",
    )
    fleet_name = models.CharField(max_length=120, blank=True, verbose_name="Fleet Name")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    current_mileage = models.IntegerField(verbose_name="Current Mileage")
    notes = models.TextField(blank=True, verbose_name="Notes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.year} {self.get_make_display()} {self.get_model_display()}"


class Maintenance(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE,
                            related_name='maintenances')
    service_name = models.CharField(
        max_length=200, verbose_name="Service Name")
    description = models.TextField(blank=True, verbose_name="Description")
    service_date = models.DateField(verbose_name="Service Date")
    cost = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Cost ($)")
    mileage_at_service = models.IntegerField(verbose_name="Mileage at Service")
    service_provider = models.CharField(
        max_length=200, blank=True, verbose_name="Service Provider")
    notes = models.TextField(blank=True, verbose_name="Notes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-service_date']

    def __str__(self):
        return f"{self.car} - {self.service_name}"


class Expense(models.Model):
    EXPENSE_TYPES = [
        ('fuel', 'Fuel'),
        ('maintenance', 'Maintenance'),
        ('insurance', 'Insurance'),
        ('registration', 'Registration'),
        ('parking', 'Parking'),
        ('other', 'Other'),
    ]

    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name='expenses')
    expense_type = models.CharField(
        max_length=20, choices=EXPENSE_TYPES, verbose_name="Type")
    description = models.CharField(max_length=200, verbose_name="Description")
    amount = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Amount ($)")
    date = models.DateField(verbose_name="Date")
    mileage = models.IntegerField(
        null=True, blank=True, verbose_name="Mileage")
    notes = models.TextField(blank=True, verbose_name="Notes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.car} - {self.description} (${self.amount})"


class FuelRecord(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="fuel_records")
    date = models.DateField(verbose_name="Date")
    odometer = models.IntegerField(verbose_name="Odometer")
    liters = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Liters")
    price_per_liter = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Price per Liter ($)"
    )
    total_cost = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Total Cost ($)"
    )
    full_tank = models.BooleanField(default=True, verbose_name="Full Tank")
    station_name = models.CharField(max_length=120, blank=True, verbose_name="Station")
    notes = models.TextField(blank=True, verbose_name="Notes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def save(self, *args, **kwargs):
        self.total_cost = self.total_cost or (self.liters * self.price_per_liter)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.car} - Fuel on {self.date} (${self.total_cost})"


class Trip(models.Model):
    TRIP_TYPE_CHOICES = [
        ("personal", "Personal"),
        ("taxi", "Taxi"),
        ("delivery", "Delivery"),
        ("ride_share", "Ride Share"),
        ("other", "Other"),
    ]

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="trips")
    date = models.DateField(verbose_name="Date")
    start_mileage = models.IntegerField(verbose_name="Start Mileage")
    end_mileage = models.IntegerField(verbose_name="End Mileage")
    distance_km = models.IntegerField(default=0, verbose_name="Distance (km)")
    income = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Income ($)"
    )
    trip_type = models.CharField(
        max_length=20, choices=TRIP_TYPE_CHOICES, default="personal", verbose_name="Trip Type"
    )
    passengers = models.PositiveSmallIntegerField(
        null=True, blank=True, verbose_name="Passengers"
    )
    notes = models.TextField(blank=True, verbose_name="Notes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def save(self, *args, **kwargs):
        self.distance_km = max(self.end_mileage - self.start_mileage, 0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.car} - {self.trip_type} on {self.date}"
