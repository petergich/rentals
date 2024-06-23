from django.db import models
from django.contrib.auth.models import User
# model for house owners
class Owner(models.Model):
    name = models.CharField(max_length=254, blank=False)
    owner_id = models.IntegerField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50, unique=True)
    profile_pic = models.ImageField(upload_to='owners/', default='owners/a.png')

    def __str__(self):
        return self.name

class House(models.Model):
    name = models.CharField(max_length=254, blank=False)
    owner = models.ForeignKey(Owner, null=True, on_delete=models.SET_NULL)
    cover_image = models.ImageField(upload_to='houses/')
    county = models.CharField(max_length=50)
    subcounty = models.CharField(max_length=50)
    ward = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    no_houses = models.IntegerField(default=0)
    no_floors=models.IntegerField(default=1)

    def __str__(self):
        return self.name

class Photo(models.Model):
    image = models.ImageField(upload_to='files/images/')
    house = models.ForeignKey(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.house)

class Tenant(models.Model):
    name = models.CharField(max_length=254)
    phone = models.CharField(max_length=50, unique=True)
    tenant_id = models.IntegerField(unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    SINGLE_ROOM = 'single_room'
    BEDSITTER = 'bedsitter'
    ONE_BEDROOM = 'one_bedroom'
    TWO_BEDROOM = 'two_bedroom'
    THREE_BEDROOM = 'three_bedroom'
    FOUR_BEDROOM = 'four_bedroom'
    FIVE_BEDROOM = 'five_bedroom'
    TYPE_CHOICES = [
        (SINGLE_ROOM, 'Single Room'),
        (BEDSITTER, 'Bedsitter'),
        (ONE_BEDROOM, 'One Bedroom'),
        (TWO_BEDROOM, 'Two Bedroom'),
        (THREE_BEDROOM, 'Three Bedroom'),
        (FOUR_BEDROOM, 'Four Bedroom'),
        (FIVE_BEDROOM, 'Five Bedroom'),
    ]
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    htype = models.CharField(max_length=20, choices=TYPE_CHOICES)
    house_number = models.CharField(max_length=50)
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    RATE_CHOICES = [
        (DAILY, "Daily"),
        (WEEKLY, "Weekly"),
        (MONTHLY, "Monthly"),
        (YEARLY, "Yearly"),
    ]
    rate = models.CharField(max_length=50, choices=RATE_CHOICES)
    price = models.IntegerField(default=0)
    floor=models.CharField(max_length=50,default="ground")

    def __str__(self): 
        return self.house_number

class Tenancy(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    is_current = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    last_charged=models.DateField(null=True)
    arrears=models.IntegerField(default=0)
    def __str__(self):
        return self.tenant.name
class Rent(models.Model):
    amount=models.IntegerField()
    amount_paid=models.IntegerField(default=0)
    cleared=models.BooleanField(default=False)
    tenancy=models.ForeignKey(Tenancy,on_delete=models.CASCADE)
    name=models.CharField(max_length=254)
    start_date=models.DateField()
    def __str__(self):
        return self.name
class Payment(models.Model):
    rent=models.ForeignKey(Rent,on_delete=models.SET_NULL,null=True)
    amount=models.IntegerField()
    date=models.DateField()
class Extra(models.Model):
    amount=models.IntegerField()
    tenancy=models.ForeignKey(Tenancy,null="True",on_delete=models.SET_NULL)