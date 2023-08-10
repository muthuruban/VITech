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
    path('admin/', views.admin_login, name='admin_login'),
    path('admin/dashboard/', views.admin_view, name='admin_dashboard'),

]
