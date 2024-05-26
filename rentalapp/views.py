from django.shortcuts import render, redirect
from django.http import HttpResponse
import csv
from django.contrib.auth.models import User
from .models import * 
from django.contrib.auth import login, authenticate,logout
from urllib.parse import urlparse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


def home(request):
    return render(request,"index.html")
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
            try:
                User.objects.create_user(username=username, email= email, password=passw)
                owner=Owner(name=name,owner_id=o_id,user=User.objects.get(email=email),phone=phone)
                owner.save()
                return redirect("ownerslogin")
            except:
                try:
                    User.objects.get(email=email).delete()
                    return render(request,"ownerregister.html",{"message":"An error occured while trying to save!"})
                except:
                    return render(request,"ownerregister.html",{"message":"An error occured while trying to save1!"})
    return render(request,"ownerregister.html")

def ownerslogin(request):
    referer = request.META.get('HTTP_REFERER')
    if referer:
        parsed_url = urlparse(referer)
        # Get the path component of the URL
        path = parsed_url.path
        # Split the path by '/' and get the last part
        last_part = path.strip('/').split('/')[-1]
        if str(last_part)== "ownerregister":
            return render(request, "ownerslogin.html", {"message": "Registered successfully"})
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None :
            if Owner.objects.filter(user=user).exists():
                login(request, user)
                return redirect('ownershome')  # Redirect to the home page after successful login
        else:
            return render(request, "ownerlogin.html", {"message": "Invalid credentials"})
    return render(request,"ownerlogin.html")
def tenantsregister(request):
    return render(request,"tenantregister.html")
def tenantslogin(request):
    return render(request,"tenantlogin.html")
def tenantshome(request):
    return HttpResponse("tenant home")
@login_required(login_url="ownerslogin")
def ownershome(request):
    try:
        owner=Owner.objects.get(user=request.user)
        o_houses=owner_houses(owner)
        return render(request, "ownershome.html",{"houses":o_houses,"owner":owner})
    except:
        logout(request)
        return redirect("ownerslogin")
@login_required(login_url="ownerslogin")
def addhouses(request):
    if request.method == "POST":
        nam=request.POST.get("name")
        img=request.POST.get("coverimage")
        county=request.POST.get("county")
        subcounty=request.POST.get("subcounty")
        ward=request.POST.get("ward")
        houses=request.POST.get("number")
        loc=request.POST.get("location")
        print("name:",nam,"\nImg:",img,"\ncounty:",county,"\nsubcounty:",subcounty,"\nward:",ward,"\nlocation:",loc)
        return render(request,"houses.html",{"locations":locations()})
    return render(request,"houses.html",{"locations":locations()})
# Create your views here.
@login_required(login_url="ownerslogin")
def tenants(request):
    return render(request,"tenants.html")
@login_required(login_url="ownerslogin")
def rooms(request):
    return render(request, "rooms.html")
@login_required(login_url="ownerslogin")
def ownersprofile(request):
    return render(request, "ownersprofile.html")
def gallery(request):
    return (request,"gallery.html")
def owner_houses(user):
    if House.objects.filter(owner=user).exists():
        return House.objects.filter(owner=user)
    else:
        return None
def subcounties(request):
    county=request.GET.get("county")
    if county:
       subcounties_instances=subcountiesdata(county)
       return JsonResponse({"data":subcounties_instances}) 
    else:
        return redirect("addhouses")
def wards(request):
    county=request.GET.get("county")
    subcounty=request.GET.get("subcounty")
    if subcounty and county:
       wards_instances=wardsdata(county,subcounty)
       return JsonResponse({"wards":wards_instances})
    else:
        return redirect("addhouses")
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
def subcountiesdata(county):
    locations_data=locations()
    for location in locations_data:
        if location["county"]==county:
            #print("found")
            subcountieslist=[]
            for sub_county in location["subcounty"]:
                subcountieslist.append(sub_county["subcounty"])
            print(subcountieslist)
            return subcountieslist
def wardsdata(county,subcounty):
    locations_data=locations()
    for location in locations_data:
        if location["county"]==county:
            #print("found")
            wards_inst=[]
            for sub_county in location["subcounty"]:
                if sub_county["subcounty"]==subcounty:
                    for ward in sub_county["wards"]:
                        wards_inst.append(ward)
                    return wards_inst