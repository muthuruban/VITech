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
    path('journal/staff/signup/', views.staff_signup, name='staff_signup'),
    # path('journal/staff/logout/', views.staff_logout, name='staff_logout'),
]
