from django.shortcuts import render, redirect
from django.http import HttpResponse
import csv
from django.contrib.auth.models import User
from .models import * 
from django.contrib.auth import login, authenticate,logout
from urllib.parse import urlparse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
message=""
def home(request):
    houses = House.objects.all()
    return render(request, "index.html", {"houses": houses})

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
        if message!="":
            alert=message
            return render(request, "ownershome.html",{"houses":o_houses,"owner":owner,"message":alert})
        return render(request, "ownershome.html",{"houses":o_houses,"owner":owner,})
    except:
        logout(request)
        return redirect("ownerslogin")
@login_required(login_url="ownerslogin")
def addhouses(request):
    try:
        owner=Owner.objects.get(user=request.user)
        o_houses=owner_houses(owner)
        if request.method == "POST":
            nam=request.POST.get("name")
            img=request.FILES.get("coverimage")
            county=request.POST.get("county")
            subcounty=request.POST.get("subcounty")
            ward=request.POST.get("ward")
            houses=request.POST.get("number")
            loc=request.POST.get("location")
            floor=request.POST.get("floors")
            latitude, longitude = map(float, loc.split(','))
            if img:
                fs = FileSystemStorage()
                image_name = fs.save(img.name, img)
                House.objects.create(
                    name=nam,
                    owner=Owner.objects.get(user=User.objects.get(username=request.user.username)),
                    cover_image=image_name,
                    county=county,
                    subcounty=subcounty,
                    no_floors=floor,
                    ward=ward,
                    latitude=latitude,
                    longitude=longitude,
                    no_houses=houses,
                    # Save the file path
                    # Save the image path
                )
                message="Successfully added"
                return redirect("ownershome")
            return render(request,"houses.html",{"locations":locations()})
        return render(request,"houses.html",{"locations":locations()})
    except:
         logout(request)
         return redirect("ownerslogin")
@login_required(login_url="ownerslogin")
def addrooms(request):
    try:
        owner=Owner.objects.get(user=request.user)
        o_houses=owner_houses(owner)
        house_id=request.GET.get("houseid")
        if house_id:
            if request.method=="POST":
                nam=request.POST.get("roomno")
                r_type=request.POST.get("roomtype")
                rate=request.POST.get("rate")
                floor=request.POST.get("floor")
                price=request.POST.get("price")
                print("name",nam,"\ntype:",r_type,"\nrate:",rate,"\nfloor:",floor,"\nprice:",price)
                Room.objects.create(
                 house=House.objects.get(id=house_id),
                 htype=r_type,
                 house_number=nam,
                 rate=rate,
                 price=price,
                 floor=floor,
                )
                
            return render(request,"addrooms.html",{"house":house_id,"floors":get_floor_names(House.objects.get(id=house_id).no_floors)})
        else:
            return redirect("ownershome")
    except:
        logout(request)
        return redirect("ownerslogin")
# Create your views here.
@login_required(login_url="ownerslogin")
def tenants(request):
    return render(request,"tenants.html")
@login_required(login_url="ownerslogin")
def rooms(request):
    try:
        owner=Owner.objects.get(user=request.user)
        o_houses=owner_houses(owner)
        house_id=request.GET.get("houseid")
        instances_rooms=Room.objects.filter(house__owner=owner)
        objects=[]
        for house in o_houses:
            i_rooms=[]
            for instance in instances_rooms:
                if instance.house==house:
                    i_rooms.append(instance)
            if i_rooms!=[]:
                objects.append({"house":house,"rooms":i_rooms})
        return render(request, "rooms.html",{"objects":objects})
    except:
         logout(request)
         return redirect("ownerslogin")
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
    csv_file_path = os.path.join(settings.BASE_DIR, 'rentalapp', 'files', 'locations.csv')
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
    county_data=os.path.join(settings.BASE_DIR, 'rentalapp', 'files', 'county_data.csv')
    county_data=os.path.join(settings.BASE_DIR, 'rentalapp', 'files', 'county_data.csv')
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
def deletehouse(request,instance_id):
    house=House.objects.get(id=instance_id)
    try:
        house.delete()
        return JsonResponse({"message":"Deleted succesfully"})
    except:
        return JsonResponse({"message":"Unable to delete, Please contact support"})
def get_floor_names(up_to_floor):
    print("floor",up_to_floor)
    # Initialize an empty list to hold the floor names
    floor_names = []
    
    # Iterate through the range from 1 to up_to_floor + 1 (inclusive)
    for floor in range(1, up_to_floor+1):
        if floor == 1:
            floor_names.append("ground")
        else:
            floor_names.append(f"{floor-1}{get_ordinal_suffix(floor-1)}")
    
    return floor_names

def get_ordinal_suffix(n):
    # Special cases for 11th, 12th, and 13th
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        # General cases
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return suffix

