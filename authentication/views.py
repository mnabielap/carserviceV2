from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
import uuid
from django.shortcuts import render, redirect
from .models import UserManage
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login

######################## INITIALIZE USER ########################
# FOR OWNER (DJANGO ADMIN)
try:
    UserManage.objects.create_superuser(username="adminForOwner4345", email="adminForOwner4345@gmail.com", password="dnrh75634!", is_owner=True)
except:
    pass
# FOR DUMMY TEKNISI 
try:
    UserManage.objects.create_user(username="tukangservis1", password="tukangservis1", is_technician=True)
except:
    pass
# FOR DUMMY STAFF 
try:
    UserManage.objects.create_user(username="staff123", password="staff123", is_staff_member=True)
except:
    pass
#################################################################

# Create your views here.
def home(request):
    try:
        user = request.user
        if user.is_technician:
            return redirect('technician:dashboard_technician')
        elif user.is_staff_member:
            return redirect('staff:dashboard_staff')
        elif user.is_owner:
            return redirect('owner:dashboard_owner')
    except:
        return render(request, 'home.html')

def login(request):
    context = dict()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            if user.is_technician:
                return redirect('technician:dashboard_technician')
            elif user.is_staff_member:
                return redirect('staff:dashboard_staff')
            else:
                return redirect('owner:dashboard_owner')
        else:
            context['status'] = 'failed'
            context['message'] = 'Terdapat kesalahan username atau password'
            return render(request, 'login.html', context=context)

    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def register(request):
    return render(request, 'register.html')

def register_technician(request):
    context = dict()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = UserManage.objects.create_user(username=username, password=password)
        except Exception as e:
            context['status'] = 'failed'
            context['message'] = 'Username sudah digunakan, coba yang lain'
            return render(request, 'register_technician.html', context=context)
        user.is_technician = True
        user.save()
        messages.success(request, 'Registration successful!')
        context = {'username': username}
        return redirect('authentication:login')
    return render(request, 'register_technician.html', context=context)

def register_staff(request):
    context = dict()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = UserManage.objects.create_user(username=username, password=password)
        except Exception as e:
            context['status'] = 'failed'
            context['message'] = 'Username sudah digunakan, coba yang lain'
            return render(request, 'register_staff.html', context=context)
        user.is_staff_member = True
        user.save()
        messages.success(request, 'Registration successful!')
        context = {'username': username}
        return redirect('authentication:login')
    return render(request, 'register_staff.html', context=context)

def register_owner(request):
    context = dict()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = UserManage.objects.create_user(username=username, password=password)
        except Exception as e:
            context['status'] = 'failed'
            context['message'] = 'Username sudah digunakan, coba yang lain'
            return render(request, 'register_owner.html', context=context)
        user.is_owner = True
        user.save()
        messages.success(request, 'Registration successful!')
        context = {'username': username}
        return redirect('authentication:login')
    return render(request, 'register_owner.html', context=context)