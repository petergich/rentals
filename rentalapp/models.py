from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Owner(models.Model):
    name=models.CharField(max_length=254)
    owner_id=models.IntegerField(unique=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    phone=models.CharField(max_length=50,unique=True)
    def __str__(self):
        return self.user
class House(models.Model):
    name=models.CharField(max_length=254)
    cover_image = models.ImageField(upload_to='files/images/')
    county=models.CharField(max_length=50)
    subcounty=models.CharField(max_length=50)
    ward=models.CharField(max_length=50)
    price=models.IntegerField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    def __str__(self):
        return self.name
class Photo(models.Model):
    image = models.ImageField(upload_to='files/images/')
    house= models.ForeignKey(Owner,on_delete=models.CASCADE)
    def __str__(self):
        return self.house
class Tenant(models.Model):
    name=models.CharField(max_length=254)
    phone=models.CharField(max_length=50,unique=True)
    tenant_id=models.IntegerField(unique=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.user
class Housetype(models.Model):
    SINGLE_ROOM = 'single_room'
    BEDSITTER = 'bedsitter'
    ONE_BEDROOM = 'one_bedroom'
    TWO_BEDROOM = 'two_bedroom'
    THREE_BEDROOM = 'three_bedroom'
    FOUR_BEDROOM = 'four_bedroom'

    TYPE_CHOICES = [
        (SINGLE_ROOM, 'Single Room'),
        (BEDSITTER, 'Bedsitter'),
        (ONE_BEDROOM, 'One Bedroom'),
        (TWO_BEDROOM, 'Two Bedroom'),
        (THREE_BEDROOM, 'Three Bedroom'),
        (FOUR_BEDROOM, 'Four Bedroom'),
    ]
    house=models.ForeignKey(House,on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    no_houses=models.IntegerField()
    def __str__(self):
        return self.house + " " +self.type
class Tenancy(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    is_current = models.BooleanField(default=True)
    start_date=models.DateField()
    end_date = models.DateField(null=True, blank=True)
    housetype=models.ForeignKey(Housetype, on_delete=models.SET_NULL,null=True, blank=True)
    def __str__(self):
        return self.tenant

