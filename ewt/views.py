from django.dispatch import receiver
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.db import IntegrityError, models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .models import CustomUser, manuData, save_uid, transactions, uid_status
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
        uidStatus(uid_list, request)

        compUid.save()

    return render(request, 'ewt/dataentry.html', {'data' : uid_dict.display_type, 'data1': uid_dict.display_spec, 
                                                    'data2': uid_dict.ram_type,'data3': uid_dict.ram_spec, 
                                                    'data4' : uid_dict.hdd_type, 'data5': uid_dict.hdd_spec, 
                                                    'data6': uid_dict.ssd_type, 'data7' : uid_dict.ssd_spec, 
                                                    'data8': uid_dict.processor_type, 'data9': uid_dict.processor_spec, 
                                                    'data10' : uid_dict.graphics_type, 'data11': uid_dict.graphics_spec, 
                                                    'data12': uid_dict.battery_type, 'data13': uid_dict.battery_spec})

def uidStatus(uid_list, request):
    save_main_uid = uid_status(username = request.user.username,
                            category = request.user.category,
                            uid = json.dumps(uid_list))
    save_main_uid.save()

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
    # usr = transactions.objects.all()
    logs = uid_status.objects.all()
    refrec = transactions.objects.all()

    ids = save_uid.objects.all()
    id = []
    for i in ids:
        # id.append(i.id)
        resp = request.POST.get(str(i.id),False)
        # print(resp,i.id)
        if resp:
            id.append(i.uid_list) 
    print(id)               
    loc = request.POST.get("location_dd")
    cat = request.POST.get("category_dd")
    print('location:',loc,'cat',cat)
    # for i in usr:
    #     if i.location == loc:
    #         setUsername = i.username
    # transaction = transactions(sender_username = request.user.username,
    #                         sender_category = request.user.category,
    #                         uid = json.dumps(uid_list),
    #                         receiver_username = setUsername,
    #                         receiver_category = request.POST.get('category_dd') )
    # transaction.save()

    return render(request, 'ewt/viewdata.html', {'logs': logs, 'refrec' : refrec})

def transfer(request, uid_list):
    usr = CustomUser.objects.all()
    # ids = save_uid.objects.all()
    # id = []
    # for i in ids:
    #     id.append(i.id)
    #     # resp = request.POST.get(i.id,False)
    #     # if resp:
    #     #     id.append(resp) 
    # print(id)               
    # loc = request.POST.get('location_dd')
    # for i in usr:
    #     if i.location == loc:
    #         setUsername = i.username
    # transaction = transactions(sender_username = request.user.username,
    #                         sender_category = request.user.category,
    #                         uid = json.dumps(uid_list),
    #                         receiver_username = setUsername,
    #                         receiver_category = request.POST.get('category_dd') )
    # transaction.save()
    return render(request, 'dataentry')

def replaceComp(request):
    return render(request, 'ewt/replace_components.html')

# LOGOUT
@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


def test_data(request):
    if request.method=="GET":
        disptype = request.GET.get("dispType", False)
        dispspec = request.GET.get("dispSpec", False)

        ramtype = request.GET.get("ramType", False)
        ramspec = request.GET.get("ramSpec", False)

        hddtype = request.GET.get("hddType", False)
        hddspec = request.GET.get("hddSpec", False)

        ssdtype = request.GET.get("ssdType", False)
        ssdspec = request.GET.get("ssdSpec", False)

        proctype = request.GET.get("procType", False)
        procspec = request.GET.get("procSpec", False)

        graphicstype = request.GET.get("graphicsType", False)
        graphicsspec = request.GET.get("graphicsSpec", False)

        batterytype = request.GET.get("batteryType", False)
        batteryspec = request.GET.get("batterySpec", False)

        if len(disptype)>0 and len(dispspec)>0 and len(ramtype)>0 and len(ramspec)>0 and len(hddtype)>0 and len(hddspec)>0 and len(ssdtype)>0 and len(ssdspec)>0 and len(proctype)>0 and len(procspec)>0 and len(graphicstype)>0 and len(graphicsspec)>0 and len(batterytype)>0 and len(batteryspec)>0:
            data = {}

            dispPost1 = uid_dict.display_type[disptype]
            dispPost2 = uid_dict.display_spec[dispspec]

            ramPost1 = uid_dict.ram_type[ramtype]
            ramPost2 = uid_dict.ram_spec[ramspec]

            hddPost1 = uid_dict.hdd_type[hddtype]
            hddPost2 = uid_dict.hdd_spec[hddspec]

            ssdPost1 = uid_dict.ssd_type[ssdtype]
            ssdPost2 = uid_dict.ssd_spec[ssdspec]

            procPost1 = uid_dict.processor_type[proctype]
            procPost2 = uid_dict.processor_spec[procspec]

            graphicsPost1 = uid_dict.graphics_type[graphicstype]
            graphicsPost2 = uid_dict.graphics_spec[graphicsspec]

            batteryPost1 = uid_dict.battery_type[batterytype]
            batteryPost2 = uid_dict.battery_spec[batteryspec]

            dispUid = dispPost1+dispPost2
            ramUid = ramPost1+ramPost2
            hddUid = hddPost1+hddPost2
            ssdUid = ssdPost1+ssdPost2
            procUid = procPost1+procPost2
            graphicsUid = graphicsPost1+graphicsPost2
            batteryUid = batteryPost1+batteryPost2
            print(dispUid)
            data = {'dispUid':dispUid, 'ramUid':ramUid, 'hddUid':hddUid, 'ssdUid':ssdUid, 'procUid':procUid, 'graphicsUid':graphicsUid, 'batteryUid':batteryUid}
        else:
            data = {'type':'abc'}

        return JsonResponse(data)

def sendToData(request):
    if request.method=="GET":
        category = request.GET.get("category", False)
        location = request.GET.get("location", False)
        setLoc = CustomUser.objects.all()
        locs = []
        comp_names = []
        for i in setLoc:
            if i.category == category:
                if i.location not in locs:
                    locs.append(i.location)
                # for j in setLoc:
        for i in setLoc:
            if i.category == category and i.location == location:
                if i.company_name not in comp_names:
                    comp_names.append(i.company_name)
        print(locs, comp_names)
        if len(category)>0:
            print(category)
            print(location)
            data = {'location':locs, 'company_name':comp_names}
        else:
            data = {'type':'abc'}
        return JsonResponse(data)


def sendData(request):
    if request.method=="GET":
        usr = CustomUser.objects.all()
        category = request.GET.get("category")
        receiver_category = request.GET.get("receiver_category")
        receiver_location = request.GET.get("receiver_location")
        print("HI ",category.split(','), " ", receiver)
        d ={'hii':'hue'}
        nums = category.split(',')
        for i in usr:
            if i.location == receiver_location and i.category == receiver_category:
                setUsername = i.username
                break
        for num in nums:
            log = save_uid.objects.get(id=num)
            transaction = transactions(sender_username = request.user.username,
                            sender_category = request.user.category,
                            uid = json.dumps(log.uid_list),
                            receiver_username = setUsername,
                            receiver_category = receiver_category )
            transaction.save()
            print(log)
        return JsonResponse(d)