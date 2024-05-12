from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Owner(models.Model):
    ownerid=models.IntegerField(unique=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.user
class House(models.Model):
    name=models.CharField(max_length=254)
    coverimage = models.ImageField(upload_to='images/')
    price=models.IntegerField()
    def __str__(self):
        return self.name
class Photos(models.Model):
    image = models.ImageField(upload_to='images/')
    house= models.ForeignKey(Owner,on_delete=models.CASCADE)
    def __str__(self):
        return self.house
class Tenants(models.Model):
    tenantid=models.IntegerField(unique=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.user
    
