import mimetypes
import os

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
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
    journals = Journals.objects.all()
    return render(request, 'staff_home.html', {'user': user, 'journals': journals})


def upload_journal(request):
    if request.method == 'POST':
        journalTitle = request.POST.get('journalTitle')
        journalISSN = request.POST.get('journalISSN')
        publisher = request.POST.get('publisher')
        department = request.POST.get('department')
        journalFile = request.FILES['journalFile']
        print(journalTitle)
        print(journalISSN)
        print(publisher)
        print(department)
        # print(journalFile)
        journal = Journals.objects.create(title=journalTitle, issn_no=journalISSN, publisher=publisher,
                                          staff=Staff.objects.get(username=request.user),
                                          department=Departments.objects.get(dept_name=department),
                                          journal_doc=journalFile)
        journal.save()
        return redirect('staff_home')
    return render(request, 'journal_form.html')


def _logout(request):
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


def download_journal(request, journal_id):
    journals = Journals.objects.get(id=journal_id)
    filename = str(journals.journal_doc)
    if filename != '':
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = BASE_DIR + '/media/' + filename
        path = open(filepath, 'rb')
        mime_type, _ = mimetypes.guess_type(filepath)
        response = HttpResponse(path, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response


def add_department(request):
    print(request.method)
    if request.method == 'POST':
        dept_number = request.POST.get('dept_number')
        dept_name = request.POST.get('dept_name')
        # dept_number = request.POST.get('dept_number')
        dept = Departments.objects.create(dept_number=dept_number, dept_name=dept_name)
        dept.save()
        return redirect('admin_dashboard')
    return render(request, 'add_department.html')
