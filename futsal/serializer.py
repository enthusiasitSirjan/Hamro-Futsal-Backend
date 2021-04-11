from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from futsal.models import *


class FutsalSerializer(ModelSerializer):
    name =serializers.CharField(source='owner.name',allow_null=True)
    class Meta:
        model = Futsal
        fields = '__all__'




class CreateFutsalSerializer(ModelSerializer):

    def validate(self, attrs):
        user = self.context.get('request').user
        futsal_exists = Futsal.objects.filter(owner=user)
        if futsal_exists:
            raise serializers.ValidationError({'error_message': 'Futsal was already added with this email'})
        else:
            return attrs

    class Meta:
        model = Futsal
        # fields = '__all__'
        exclude = ['owner']


class BookingFutsalSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class UserBookingFutsalSerializer(ModelSerializer):
    def validate(self, attrs):
        booking = dict(attrs)
        if UserBooking.objects.filter(futsal=booking["futsal"],user_book_date = booking["user_book_date"],user_book_time =booking["user_book_time"],status="Approved"):

            raise serializers.ValidationError({'error_message': 'Already booked for this time'})

        else:
            return attrs


    class Meta:
        model = UserBooking
        exclude = ['booked_by']


class ListMyBookingSerializer(ModelSerializer):
    futsal_name = serializers.CharField(source="futsal.futsal_name", allow_null=True)
    location = serializers.CharField(source="futsal.location", allow_null=True)
    futsal_rate = serializers.CharField(source="futsal.futsal_rate", allow_null=True)
    name = serializers.CharField(source='booked_by.name',allow_null=True)
    class Meta:
        model = UserBooking
        fields = "__all__"


class OwnerBookingFutsalSerializer(ModelSerializer):
    name = serializers.CharField(source='booked_by.name', allow_null=True)
    phone_number = serializers.CharField(source='booked_by.phone_number', allow_null=True)

    class Meta:
        model = UserBooking
        fields = '__all__'


class TrainingSerializer(ModelSerializer):
    class Meta:
        model = Trainings
        fields = '__all__'


class TournamentSerializer(ModelSerializer):
    class Meta:
        model = Tournaments
        fields = '__all__'


class FutsalMembership(ModelSerializer):
    def validate(self, attrs):
        membership = dict(attrs)
        if Membership.objects.filter(futsal=membership["futsal"], member_type=membership["member_type"]):
            raise serializers.ValidationError({'error_message': 'You have already been a member'})

        else:
            return attrs
    class Meta:
        model = Membership
        exclude = ['member']


class ShowMembers(ModelSerializer):
    name = serializers.CharField(source='member.name', allow_null=True)
    phone_number = serializers.CharField(source='member.phone_number', allow_null=True)
    email = serializers.CharField(source='member.email', allow_null=True)
    address = serializers.CharField(source='member.address', allow_null=True)

    class Meta:
        model = Membership
        fields = "__all__"



