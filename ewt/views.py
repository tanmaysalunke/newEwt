from unicodedata import category
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.db import IntegrityError
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
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
            # groups = Group.objects.get(name=request.POST.get('access_level'))
            # groups.user_set.add(user_reg)
            return render(request, "ewt/login.html")
        except IntegrityError:
            messages.info(request, "Username already present!")
    return render(request, "ewt/register.html")


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = CustomUser.objects.get(username=username)

        # print(user.category)
        #category based access to pages:
        if user.category == 'Manufacturer':
            return render(request, 'manufacturer.html')
        elif user.category == 'Refurbisher':
            return render(request, 'refurbisher.html')
        elif user.category == 'Recycler':
            return render(request, 'recycler.html')

            
        # implement try catch for username validation

        if check_password(password, user.password) is True:
            login(request, user)
            return redirect('base.html')
        else:
            messages.info(request, 'Username or Password is incorrect')
    return render(request, 'ewt/login.html')


# LOGOUT
@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')
