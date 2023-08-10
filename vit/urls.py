from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from journal import views

app_name = 'journal'

urlpatterns = [
    # Index Page
    path('', views.index, name='index'),

    # Staff
    path('staff/signup/', views.staff_signup, name='staff_signup'),
    path('staff/home/', views.staff_home, name='staff_home'),

    # Admin
    path('admin/', views.admin_login, name='admin_login'),
    path('admin/dashboard/', views.admin_view, name='admin_dashboard'),
    path('admin/dashboard/add_department/', views.add_department, name='add_department'),

]
