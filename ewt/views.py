from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.db import IntegrityError, models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .models import CustomUser, manuData, save_uid, transactions
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from . import uid_dict
import json

# Create your views here.

def registerPage(request):
    if request.method == 'POST':
        user_reg = CustomUser.objects.create_user(first_name=request.POST.get('first_name'),
                        last_name=request.POST.get('last_name'),
                        password=request.POST.get('password1'),
                        email=request.POST.get('email'),
                        username=request.POST.get('username'),
                        location=request.POST.get('location'),
                        company_name=request.POST.get('company_name'),
                        category=request.POST.get('access_level'))
        try:
            user_reg.save()
            return redirect(loginPage)
        except IntegrityError:
            messages.info(request, "Username already present!")
    return render(request, "ewt/register.html")


def dataEntry(request):
    if request.method == 'POST':
        compUid = manuData(display_uid = request.POST.get('display_uid'),
                            ram_uid = request.POST.get('ram_uid'),
                            hdd_uid = request.POST.get('hdd_uid'),
                            ssd_uid = request.POST.get('ssd_uid'),
                            processor_uid = request.POST.get('processor_uid'),
                            graphics_uid = request.POST.get('graphics_uid'),
                            battery_uid = request.POST.get('battery_uid'))

        display_uid = request.POST.get('display_uid')
        ram_uid = request.POST.get('ram_uid')
        hdd_uid = request.POST.get('hdd_uid')
        ssd_uid = request.POST.get('ssd_uid')
        processor_uid = request.POST.get('processor_uid')
        graphics_uid = request.POST.get('graphics_uid')
        battery_uid = request.POST.get('battery_uid')
        uid_list = [display_uid, ram_uid, hdd_uid, ssd_uid, processor_uid, graphics_uid, battery_uid]
        saveUid(uid_list, request)

        compUid.save()

    return render(request, 'ewt/dataentry.html', {'data' : uid_dict.display_type, 'data1': uid_dict.display_spec, 
                                                    'data2': uid_dict.ram_type,'data3': uid_dict.ram_spec, 
                                                    'data4' : uid_dict.hdd_type, 'data5': uid_dict.hdd_spec, 
                                                    'data6': uid_dict.ssd_type, 'data7' : uid_dict.ssd_spec, 
                                                    'data8': uid_dict.processor_type, 'data9': uid_dict.processor_spec, 
                                                    'data10' : uid_dict.graphics_type, 'data11': uid_dict.graphics_spec, 
                                                    'data12': uid_dict.battery_type, 'data13': uid_dict.battery_spec})

def saveUid(uid_list, request):
    save_main_uid = save_uid(username = request.user.username,
                            category = request.user.category,
                            uid_list = json.dumps(uid_list))
    save_main_uid.save()

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = CustomUser.objects.get(username=username)
            if check_password(password, user.password) is True:
                login(request, user)
                #category based access to pages:
                if user.category == 'Manufacturer':
                    return redirect('dashboard')
                elif user.category == 'Refurbisher':
                    return redirect('dashboard')
                    # return render(request, 'ewt/Refurbisher.html')
                elif user.category == 'Recycler':
                    return redirect('dashboard')
                    # return render(request, 'ewt/recycler.html')
            else:
                messages.info(request, 'Username or Password is incorrect')

        except ObjectDoesNotExist:
            messages.info(request, "Username does not exist!")

        
        # print(user.category)

        # implement try catch for username validation
        
        
    return render(request, 'ewt/login.html')

def dashboard(request):
    return render(request, 'ewt/dashboard.html')

def viewdata(request):
    logs = save_uid.objects.all()
    refrec = CustomUser.objects.all()
    # for loc in refrec:
    #     print(loc.location)
    return render(request, 'ewt/viewdata.html', {'logs': logs, 'refrec' : refrec})

def transfer(request, uid_list):
    transaction = transactions(sender_username = request.user.username,
                            sender_category = request.user.category,
                            uid = json.dumps(uid_list),
                            receiver_username = request.user.username,
                            receiver_category = request.user.category )
    transaction.save()
    return render(request, 'dataentry')

def replaceComp(request):
    return render(request, 'ewt/replace_component.html')

# LOGOUT
@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


