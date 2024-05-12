from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request,"landing.html")
def ownersregister(request):
    return HttpResponse("Owners Register")
def ownerslogin(request):
    return HttpResponse("Owners Login")
def tenantsregister(request):
    return HttpResponse("Tenants Register")
def tenantslogin(request):
    return HttpResponse("Tenants Login")
# Create your views here.
