from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from journal.forms import StaffLoginForm, StaffSignupForm, AdminLoginForm
from journal.models import Departments, Journals, Staff


# Create your views here.
def index(request):
    if request.method == 'POST':
        form = StaffLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login Successful')
                return redirect('staff_home')
            else:
                messages.error(request, 'Invalid username or password')
                form.add_error(None, 'Invalid username or password')
    else:
        form = StaffLoginForm()
    return render(request, 'index.html', {'form': form})


def staff_signup(request):
    departments = Departments.objects.all()
    if request.method == 'POST':
        form = StaffSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account has been successfully created')
            return redirect('index')
        else:
            print(form.errors)
    else:
        form = StaffSignupForm()
    return render(request, 'staff_signup.html', {'form': form, 'departments': departments})


@login_required(login_url='index')
def staff_home(request):
    user = Staff.objects.get(username=request.user)
    return render(request, 'staff_home.html', {'user': user})


def staff_logout(request):
    logout(request)
    return redirect('index')


def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = AdminLoginForm()
    return render(request, 'admin_login.html', {'form': form})


@login_required(login_url='admin_login')
def admin_view(request):
    journals = Journals.objects.all()
    departments = Departments.objects.all()
    return render(request, 'admin_dashboard.html', {'journals': journals, 'departments': departments})


def add_department(request):
    print(request.method)
    if request.method == 'POST':
        dept_number = request.POST.get('dept_number')
        dept_name = request.POST.get('dept_name')
        # dept_number = request.POST.get('dept_number')
        dept = Departments.objects.create(dept_number=dept_number, dept_name=dept_name)
        dept.save()
        return redirect('index')
    return render(request, 'admin_dashboard.html')
