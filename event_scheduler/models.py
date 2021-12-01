from django.db import models
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db.models.fields.related import ForeignKey
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail 
from django.conf import settings

from django.contrib.auth.models import BaseUserManager


from event_scheduler import utils
from django.utils.translation import gettext_lazy as _
from bootstrap_datepicker_plus import DatePickerInput, DateTimePickerInput
from django.contrib.auth import get_user_model
from django_rest_passwordreset.tokens import get_token_generator
from django import forms
from datetime import datetime



class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name,)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.is_vaccinated = False
        user.save(using=self._db)

        return user

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_vaccinated = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name for user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of user"""
        return self.email

class MeetingRoom(models.Model):
    Room_number = models.CharField(
        max_length=5,
        unique=True
    )
    class ROOM_T(models.TextChoices):
        DESK  = 'DESK ',_('DESK')
        CONFRENCE = 'CONFRENCE ROOM',_('CONFRENCE')
    Room_Types = models.CharField(max_length=14,choices=ROOM_T.choices,default=ROOM_T.CONFRENCE,)
    Floor = models.CharField(max_length=2,unique=True)
    capacity = models.IntegerField(blank=False)
    Availability = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.Room_number)
        
    def get_absolute_url(self):
        return reverse('room-details', kwargs={'room_number': self.Room_number})

    
class BookingItem(models.Model):
    User_profile = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    related_name='User_profile',
    on_delete=models.CASCADE
    )
    class BUSINESS(models.TextChoices):
        IT = 'IT', _('Information Technology')
        HR = 'HR', _('Human_Resource')
        FIN = 'FIN', _('Finance')
        MK = 'MK', _('Marketing')
        DG = 'DG', _('Digital')
    Booking_id = models.CharField(max_length = 10,unique=True,default=utils.create_new_ref_number)
    Business_unit = models.CharField(max_length=3,choices=BUSINESS.choices,default=BUSINESS.IT,)
    Room_number = models.OneToOneField(MeetingRoom,to_field='Room_number', related_name='Room', on_delete=models.CASCADE)
    Date = models.DateField("Date")
    time_choice = (
       (1, '8:00'),
       (2, '9:00'),
       (3, '10:00'),
       (4, '11:00'),
       (5, '12:00'),
       (6, '13:00'),
       (7, '14:00'),
       (8, '15:00'),
       (9, '16:00'),
       (10, '17:00'),
       (11, '18:00'),
       (12, '19:00'),
       (13, '20:00'),
      )     
    time_id = models.IntegerField(choices=time_choice)
    Duration = models.IntegerField(default=1)
    
    def __str__(self):
        return (self.Booking_id)
    def get_absolute_url(self):
        return reverse('BookingItem-details', kwargs={'id': self.id})