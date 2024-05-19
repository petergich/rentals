from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("ownerslogin", views.ownerslogin,name="ownerslogin"),
    path("ownersregister", views.ownersregister, name="ownersregister"),
    path("ownershome",views.ownershome,name="ownershome"),
    path("tenantslogin", views.tenantslogin,name="tenantslogin"),
    path("tenantsregister",views.tenantsregister, name="tenanatsregister"),
    path("addhouses",views.addhouses,name="addhouses"),
    path("tenants",views.tenants,name="tenants"),
    path("rooms",views.rooms,name="rooms"),
    path("ownersprofile",views.ownersprofile,name="ownersprofile"),
    path("gallery",views.gallery,name="gallery"),
    path("subcounties",views.subcounties,name="subcounties"),
    path("wards",views.wards,name="wards")
]
