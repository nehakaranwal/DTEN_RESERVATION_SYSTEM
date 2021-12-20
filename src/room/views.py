

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404

# Create your views here.
from event_scheduler.models import MeetingRoom,Meeting, UserProfile
from .forms import CreateRoomModelForm
import requests
from django.contrib import messages


def room_list_view(request):
    queryset = MeetingRoom.objects.all()
    print(queryset)
    title = "Meeting room list"
    template_name = 'list-room.html'
    context = {
        'title': title,
        'object_list': queryset
    }
    return render(request, template_name, context)


@login_required
def room_create_view(request):
    template_name = 'create.html'
    form = CreateRoomModelForm(request.POST or None)
    user_list = UserProfile.objects.filter(email=request.user)
    for obj in user_list:
        print(obj)
        if not obj.is_superuser:
                messages.error(request,f"{obj.username} is not SuperUser.Access has been restricted.Please contact admin")
                return redirect("room:room-list")
    if form.is_valid():
        data = request.POST.copy()
        form.user = request.user
        form.save()
        form = CreateRoomModelForm()
        return redirect("room:room-list")
    context = {
        "title": "Create new room",
        "form": form
    }
    return render(request, template_name, context)


def room_detail_view(request, Room_number):
    user = request.user
    print(user)
    title = "Details of " + str(Room_number) + " meeting room"
    obj = get_object_or_404(MeetingRoom, Room_number=Room_number)
    print(obj)
    availbility_list = Meeting.objects.filter(Room_number_id=obj)
    print(availbility_list)
    template_name = 'detail_room.html'
    context = {
        'title': title,
        'object': obj,
        'availbility_list': availbility_list
    }
    return render(request, template_name, context)


@login_required
def room_update_view(request, Room_number):
    title = "Updating " + str(Room_number) + " meeting room"
    obj = get_object_or_404(MeetingRoom, Room_number=Room_number)
    form = CreateRoomModelForm(request.POST or None, instance=obj)
    user_list = UserProfile.objects.filter(email=request.user)
    for obj in user_list:
        print(obj)
        if not obj.is_superuser:
                messages.error(request,f"{obj.username} is not SuperUser.Access has been restricted.Please contact admin")
                return redirect("room:room-list")
    if form.is_valid():
        form.save()
        return redirect("room:room-list")
    template_name = 'create_room.html'
    context = {
        'title': title,
        'object': obj,
        'form': form,
    }
    return render(request, template_name, context)


@login_required
def room_delete_view(request, Room_number):
    title = "Deleting " + str(Room_number) + " meeting room"
    obj = get_object_or_404(MeetingRoom, Room_number=Room_number)
    user_list = UserProfile.objects.filter(email=request.user)
    for obj in user_list:
        print(obj)
        if not obj.is_superuser:
                messages.error(request,f"{obj.username} is not SuperUser.Access has been restricted.Please contact admin")
                return redirect("room:room-list")
    template_name = 'delete_room.html'
    if request.method == "POST":
        obj.delete()
        return redirect("room:room-list")
    context = {
        'title': title,
        'object': obj
    }
    return render(request, template_name, context)