from django.urls import path, include
from . import views


urlpatterns = [
    path("logout", views.user_logout, name="logout"), 
    path("", views.home, name="home"),
    path("login",views.route,name="route"),
    path("ownerslogin", views.ownerslogin,name="ownerslogin"),
    path("ownersregister", views.ownersregister, name="ownersregister"),
    path("ownershome",views.ownershome,name="ownershome"),
    path("tenantslogin", views.tenantslogin,name="tenantslogin"),
    path("tenantsregister",views.tenantsregister, name="tenantsregister"),
    path("addhouses",views.addhouses,name="addhouses"),
    path("tenants",views.tenants,name="tenants"),
    path("rooms",views.rooms,name="rooms"),
    path("ownersprofile",views.ownersprofile,name="ownersprofile"),
    path("gallery",views.gallery,name="gallery"),
    path("subcounties",views.subcounties,name="subcounties"),
    path("wards",views.wards,name="wards"),
    path('delete/<int:instance_id>/', views.deletehouse, name='delete_model_instance'),
    path("addrooms",views.addrooms,name="addrooms"), 
    path("room",views.room,name="room"),
    path("addtenant",views.addtenant,name="addtenant"),
    path("gettenant",views.gettenant,name="gettenant"),
]
