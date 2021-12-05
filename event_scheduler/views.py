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
import requests
from .forms import CreateReservationModelForm,CreateUserModelForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BookingItem, UserProfile,Meeting

from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from datetime import datetime,date

from django.views.decorators.csrf import csrf_exempt
from .signals import send_update



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
    else:
        user = request.user
        queryset = BookingItem.objects.filter(User_profile=user.id)
        user_list = UserProfile.objects.all()
        if user.is_vaccinated:
            pass
        else:
            messages.error(request,f"{user} is not vaccinated.")
            return redirect("event_scheduler:user_login_view")
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
            queryset = BookingItem.objects.filter(User_profile=user.id)
            print(type(queryset))
            tot_book = []
            tot_book = queryset
            if len(tot_book) <= 4:
                pass
            else:
                messages.error(request,f"{user} has exceeded the limit of maximum 5 booking.")
                return redirect("event_scheduler:reservation-list")
            if len(data['Date_month']) < 2:
                    data['Date_month'] = '0' + data['Date_month']
                    print(data['Date_month'])
            date_str = data['Date_year'] + '-' + data['Date_month'] + '-' + data['Date_day']
            temp_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            print(temp_date)
            print(date.today())
            if  temp_date < date.today():
                    messages.error(request,"Please select the current/future date")
                    return redirect("event_scheduler:reservation-create")
            queryset2 = Meeting.objects.filter(Room_number=data['Room_number'])
            cnt = 0
            for object in queryset2:
                cnt = cnt + 1
                Meeting_list=object
                print((Meeting_list.available_date))
                print(int(data["time_id"]) + int(data["Duration"]))
                #or ((int(data['time_id']) + int(data['Duration'])) <= Meeting_list.available_time_id)
                if (temp_date == Meeting_list.available_date) and (int(data['time_id']) == Meeting_list.available_time_id):
                    print(Meeting_list.id)
                    Meeting.objects.filter(id=Meeting_list.id).delete()
                    break
                elif len(queryset2) == cnt:
                    messages.error(request,f"Meeting Room {Meeting_list.Room_number} has been booked for the given time.Please visit the meeting room page to check available time slots")
                    return redirect("event_scheduler:reservation-list")
                
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
        messages.info(request, f"Booking has been updated.")
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
        messages.info(request, f"Booking has been deleted.")
        return redirect('/event_scheduler')
    context = {
        'title': title,
        'object': obj
    }
    return render(request, template_name, context)




