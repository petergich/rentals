from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("ownerslogin", views.ownerslogin,name="ownerslogin"),
    path("ownersregister", views.ownersregister, name="ownersregister"),
    path("tenantslogin", views.tenantslogin,name="tenantslogin"),
    path("tenantsregister",views.tenantsregister, name="tenanatsregister"),
]
