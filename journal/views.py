from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect

from journal.forms import StaffLoginForm, StaffSignupForm, AdminLoginForm


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
    return render(request, 'staff_signup.html', {'form': form})


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


def admin_view(request):
    return render(request, 'admin_dashboard.html')
