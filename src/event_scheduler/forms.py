from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import BookingItem,MeetingRoom,UserProfile
from django.contrib.admin.widgets import AdminDateWidget



class CreateUserModelForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = UserProfile
        fields = ("username", "email", "password1", "password2")
    
    def save(self, commit=True):
	    user = super(CreateUserModelForm, self).save(commit=False)
	    user.email = self.cleaned_data['email']
	    if commit:
		    user.save()
	    return user


class LoginUserModelForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'email',
            'password',
        ]
        widgets = {
            'password': forms.PasswordInput(),
        }
        

class CreateReservationModelForm(forms.ModelForm):
     class Meta:
         model = BookingItem
         exclude = ("User_profile",)
         fields = '__all__'
         widgets = {
            'Booking_id' : forms.TextInput(attrs={'readonly': 'readonly'}),
            'Date': forms.SelectDateWidget(empty_label="Not set", months=None),
        }