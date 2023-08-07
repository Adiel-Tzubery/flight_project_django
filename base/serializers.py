from rest_framework import serializers
from .models import *


class FlightModelSerializer(serializers.ModelSerializer):
    # serialize the names rather than the ID's 
    origin_country = serializers.CharField(source='origin_country.name')
    destination_country = serializers.CharField(source='destination_country.name')
    airline_company = serializers.CharField(source='airline_company.name')

    # Serialize departure_time and landing_time with a user-friendly format
    departure_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    landing_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    
    class Meta:
        model = Flight
        fields = [
            'id',
            'origin_country',
            'destination_country',
            'airline_company',
            'departure_time',
            'landing_time',
            'price',
            'remaining_tickets'
        ]


class AirlineCompanyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirlineCompany
        fields = '__all__'


class CountryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class UserModelSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='get_user_role_name')
    user_id = serializers.IntegerField(source='id')

    class Meta:
        model = User
        fields = [
            'user_id',
            'email',
            'username',
            'role_name',
            'profile_pic'
        ]


class CustomerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class AdministratorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrator
        fields = '__all__'


class TicketModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
