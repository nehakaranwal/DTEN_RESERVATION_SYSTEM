from django import forms
from event_scheduler.models import MeetingRoom


class CreateRoomForm(forms.Form):
    room_number = forms.ModelChoiceField(queryset=MeetingRoom.objects.all())
    capacity = forms.IntegerField()


class CreateRoomModelForm(forms.ModelForm):
    class Meta:
        model = MeetingRoom
        fields = ['Room_number','Floor','capacity','Room_Types','Availability']