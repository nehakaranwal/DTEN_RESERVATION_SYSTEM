from django.contrib import admin

# Register your models here.

from django.contrib.admin import AdminSite
from django.contrib.auth import views as auth_views
from django.urls import path
from event_scheduler import models

class MyAdminSite(AdminSite):
    site_header = 'Welcome to DTEN Desk Reservation System'
    

admin_site = MyAdminSite(name='myadmin')

admin_site.register(models.UserProfile)
admin_site.register(models.BookingItem)
admin_site.register(models.MeetingRoom)
