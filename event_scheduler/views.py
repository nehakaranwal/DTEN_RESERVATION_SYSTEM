from rest_framework.views import APIView
from rest_framework.response import Response
from event_scheduler import models
from rest_framework import viewsets
from event_scheduler import serializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from event_scheduler import permissions
from rest_framework import filters
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
import requests
from .forms import CreateReservationModelForm,CreateUserModelForm
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BookingItem, UserProfile

from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from rest_framework.decorators import action
import datetime

from django.views.decorators.csrf import csrf_exempt



class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating, creating and updating profiles"""
    serializer_class = serializer.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)

class UserBookingItemViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializer.BookingItemSerializer
    queryset = models.BookingItem.objects.all()
    permission_classes = (permissions.UpdateOwnProfile,IsAuthenticated,)
    
    
class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = serializer.RoomSerializer
    queryset = models.MeetingRoom.objects.all()

def user_create_view(request):
	if request.method == "POST":
		form = CreateUserModelForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user, backend='django.contrib.auth.backends.ModelBackend')
			messages.success(request, "Registration successful." )
			return redirect("event_scheduler:user_login_view")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = CreateUserModelForm()
	return render (request=request, template_name="create_user.html", context={"register_form":form})
    

@csrf_exempt
def user_login_view(request):
    if request.method == "POST":
	    form = AuthenticationForm(request, data=request.POST)
	    if form.is_valid():
		    username = form.cleaned_data.get('username')
		    password = form.cleaned_data.get('password')
		    user = authenticate(request,username=username, password=password)
		    if user is not None:
			    login(request, user)
			    messages.info(request, f"You are now logged in as {username}.")
			    return redirect("event_scheduler:reservation-list")
		    else:
			    messages.error(request,"Invalid username or password.")
	    else:
		    messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})


def user_logout(request):
    logout(request)
    messages.info(request, f"You are now logout.Please login again")
    return redirect("event_scheduler:user_login_view")

@login_required
def reservation_list_view(request):
    if request.GET.get('user-filter'):
        user_filter = request.GET.get('user-filter')
        queryset = BookingItem.objects.filter(User_profile=user_filter)
        print
    else:
        user = request.user
        queryset = BookingItem.objects.filter(User_profile=user.id)
        user_list = UserProfile.objects.all()
    title = "Reservations list"
    template_name = 'list.html'
    context = {
        'title': title,
        'object_list': queryset,
        'user_list': user_list
    }
    print(user_list)
    print(queryset)
    return render(request, template_name, context)


@login_required
def reservation_create_view(request):
    template_name = 'create.html'
    form = CreateReservationModelForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            data = request.POST.copy()
            user = request.user
            print(user)
            data.update({'User_profile_id': int(user.id)})
            doc=form.save(commit=False)
            doc.User_profile_id = int(user.id)
            doc.save()
            response = requests.post(
                'http://localhost:8000/event_scheduler/', data=data)
            content = response.content
            messages.info(request, f"Booking has been confirmed.")
            return redirect("event_scheduler:reservation-list")
    context = {
        "title": "Create new reservation",
        "form": form
    }
    return render(request, template_name, context)


def reservation_detail_view(request,id, *Room_number):
    title = "Details of " + str(Room_number) + " meeting room"
    obj = get_object_or_404(BookingItem, id=id)
    template_name = 'detail.html'
    context = {
        'title': title,
        'object': obj
    }
    return render(request, template_name, context)


@login_required
def reservation_update_view(request, *Room_number, id):
    title = "Updating " + str(Room_number) + " room reservation"
    obj = get_object_or_404(BookingItem, id=id)
    form = CreateReservationModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/event_scheduler')
    template_name = 'create.html'
    context = {
        'title': title,
        'object': obj,
        'form': form,
    }
    return render(request, template_name, context)


@login_required
def reservation_delete_view(request, *room_number, id):
    title = "Deleting " + str(room_number) + " meeting room"
    obj = get_object_or_404(BookingItem, id=id)
    template_name = 'delete.html'
    if request.method == "POST":
        obj.delete()
        return redirect('/event_scheduler')
    context = {
        'title': title,
        'object': obj
    }
    return render(request, template_name, context)




