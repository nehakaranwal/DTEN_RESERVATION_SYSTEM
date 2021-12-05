from django.core.mail import EmailMessage
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.db.models.signals import post_save,post_delete
from .models import BookingItem
from web_project.settings import DEFAULT_FROM_EMAIL

from event_scheduler import models
from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
import datetime
from django.http import request
from django.template.loader import render_to_string



@receiver(post_save,sender=BookingItem)    
def send_update(sender,instance, **kwargs):
    booking = instance
    context = {'booking':booking}
    message = render_to_string("booking_conf.html",context)
    Body = message
    Subject = "Booking Confirmation" 
    from_email = DEFAULT_FROM_EMAIL
    email = booking.User_profile
    message = EmailMessage(subject=Subject,body=Body,from_email=from_email,to=[email])
    message.content_subtype = "html"
    return message.send()


@receiver(post_delete,sender=BookingItem)
def send_delete(sender,instance, **kwargs):
    booking = instance
    context = {'booking':booking}
    message = render_to_string("booking_del_conf.html",context)
    Body = message
    Subject = "Booking Cancelled" 
    from_email = DEFAULT_FROM_EMAIL
    email = booking.User_profile
    message = EmailMessage(subject=Subject,body=Body,from_email=from_email,to=[email])
    message.content_subtype = "html"
    return message.send()