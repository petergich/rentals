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
    # house_type=
    # county=
    # subcounty=
    # ward=
    # longitude=
    # latitude=
    price=models.IntegerField()
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
class Tenancy(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    is_current = models.BooleanField(default=True)
    start_date=models.DateField()
    end_date = models.DateField(null=True, blank=True) 
    def __str__(self):
        return self.tenant
