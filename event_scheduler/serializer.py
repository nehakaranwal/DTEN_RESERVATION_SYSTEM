from rest_framework import serializers
from event_scheduler import models
from django.contrib.auth import password_validation



class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing out APIView"""
    name = serializers.CharField(max_length=10)

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ('id','email', 'name', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        return user
    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)

    #def save(self, *args, **kwargs):  
    #   super(models.UserProfile, self).save(*args, **kwargs) # Call the real save() method


class BookingItemSerializer(serializers.ModelSerializer):
    """Serializes Booking Entry items"""
    # Room_number=serializers.ReadOnlyField(source='MeetingRoom.Room_number')

    # class Meta:
    #     model = models.BookingItem
    #     fields = ('User_profile', 'Booking_id','Business_unit','Room_number', 'Date','Time_id')
    #     extra_kwargs = {'User_profile': {'read_only': True}}
    #     read_only_fields = ['Booking_id']
    
    class Meta:
        model = models.BookingItem

    def to_representation(self, instance):
        representation = dict()
        representation["id"] = instance.id
        representation["User_profile"] = instance.UserProfile.email
        representation["Booking_id"] = instance.Booking_id
        representation["Business_unit"] = instance.Business_unit
        representation["Date"] = instance.Date
        representation["Time_id"] = instance.Time_id

        return representation
        
        
        
    
class RoomSerializer(serializers.ModelSerializer):
    Room_number = serializers.IntegerField()
    Floor = serializers.IntegerField()
    capacity = serializers.IntegerField()

    class Meta:
        model = models.MeetingRoom
        fields = [
            'url',
            'Room_number',
            'Floor',
            'capacity',
            'Room_Types'
        ]

        