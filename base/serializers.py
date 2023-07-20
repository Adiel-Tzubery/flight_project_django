from rest_framework import serializers
from .models import *


class FlightModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'


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

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'role_name'
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
