from django.shortcuts import render
from django.http import HttpResponse
import csv
from django.contrib.auth.models import User
from .models import *




def home(request):
    return render(request,"landing.html")
def ownersregister(request):
    if request.method=="POST":
        username=request.POST.get("username")
        name=request.POST.get("name")
        email=request.POST.get("email")
        o_id=request.POST.get("nid")
        passw=request.POST.get("password")
        phone=request.POST.get("phone")
        if User.objects.filter(email=email).exists():
            return render(request,"ownerregister.html",{"message":"An owner with the email already exists"})
        if Owner.objects.filter(owner_id=o_id).exists():
            return render(request,"ownerregister.html",{"message":"An owner with the id already exists"})
        if User.objects.filter(username=username).exists():
            return render(request,"ownerregister.html",{"message":"An owner with the username already exists"})
        else:
            #try:
                User.objects.create_user(username=username, email= email, password=passw)
                owner=Owner(name=name,owner_id=o_id,user=User.objects.get(email=email),phone=phone)
                owner.save()
            # except:
            #     try:
            #         User.objects.get(email=email).delete
            #         return render(request,"ownerregister.html",{"message":"An error occured while trying to save!"})
            #     except:
            #         return render(request,"ownerregister.html",{"message":"An error occured while trying to save!"})
    return render(request,"ownerregister.html")
def ownerslogin(request):
    return render(request,"ownerlogin.html")
def tenantsregister(request):
    return render(request,"tenantregister.html")
def tenantslogin(request):
    return render(request,"tenantlogin.html")
def tenantshome(request):
    return HttpResponse("tenant home")
def ownershome(request):
    return HttpResponse("Owner home")
# Create your views here.
def locations():


    # Define the path to your CSV file
    csv_file_path = "C:/Users/CCAdmin/projects/rentals/rentalapp/files/locations.csv"

    # Create an empty list to store the data
    data = []

    # Open the CSV file
    with open(csv_file_path, newline='') as csvfile:
        # Create a CSV reader object
        reader = csv.reader(csvfile)
        
        # Iterate over each row in the CSV file
        for row in reader:
            # Append the row to the data list
            data.append(row)
    # Initialize an empty dictionary
    val=1
    county_dict={}
    county_data="C:/Users/CCAdmin/projects/rentals/rentalapp/files/county_data.csv"
    with open(county_data, newline='') as csvfile:
        # Create a CSV reader object
        county_dat= csv.reader(csvfile)
        jump=0
        for row in county_dat:
            if jump==0:
                jump=jump+1
                continue
            code, county=row
            county_dict[val]=county
            val=val+1
            jump=jump+1
    # Print the resulting dictionary
    print(county_dict)
    # Now you can access the data variable which contains the data from the CSV file
    # For example, to print the first 5 rows:
    locations=[]
    count=1
    for county in county_dict:
        subcounties=[]
        for row in data[48:]:
            areaid, code, subcounty, ward = row
            
            if int(code)== count:
                if subcounty in subcounties:
                    continue
                else:
                    subcounties.append(subcounty)
            else:
                continue
        c_subcounties=[]
        for subcount in subcounties:
            wards=[]
            for row in data[48:]:
                areaid, code, subcounty, ward = row
                if int(code)== count:
                    if subcounty == subcount and ward not in wards:
                        wards.append(ward)
            c_subcounties.append({"subcounty":subcount,"wards":wards})
        locations.append({"county":county_dict[county],"subcounty":c_subcounties})   
        count=count+1
    return locations