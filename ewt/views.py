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
            return render(request, "ewt/login.html")
        except IntegrityError:
            messages.info(request, "Username already present!")
    return render(request, "ewt/register.html")


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = CustomUser.objects.get(username=username)

        name = user.first_name
        # print(user.category)

        # implement try catch for username validation

        if check_password(password, user.password) is True:
            login(request, user)
            #category based access to pages:
            if user.category == 'Manufacturer':
                return render(request, 'ewt/Manufacturer.html', {'user_name' : name})
            elif user.category == 'Refurbisher':
                return render(request, 'ewt/Refurbisher.html', {'user_name' : name})
            elif user.category == 'Recycler':
                return render(request, 'ewt/recycler.html', {'user_name' : name})
        else:
            messages.info(request, 'Username or Password is incorrect')
    return render(request, 'ewt/login.html')


# LOGOUT
@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')
