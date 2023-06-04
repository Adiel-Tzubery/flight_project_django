from django.shortcuts import render
from facads.facade_base import FacadeBase
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.serializers import FlightModelSerializer, AirlineCompanyModelSerializer, CountryModelSerializer



# @@@ facade base views @@@


@api_view(['GET'])
def get_all_flights(): # do the function need to get a request?
    flights = FacadeBase.get_all_flights()
    serializer = FlightModelSerializer(flights, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_flight_by_id(request, id):
    flight = FacadeBase.get_flight_by_id(id)
    serializer = FlightModelSerializer(flight, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def get_flights_by_parameters(request, origin_country_id=None, destination_country_id=None, date=None):
    flights = FacadeBase.get_airline_by_parameters(origin_country_id=None, destination_country_id=None, date=None)
    serializer = FlightModelSerializer(flights, many=True) # what to do for cases where thee is 0/1 flights in the many=?
    return Response(serializer.data)


@api_view(['GET'])
def get_all_airlines(request):
    airlines = FacadeBase.get_all_airlines()
    serializer = AirlineCompanyModelSerializer(airlines, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_airline_by_id(id):
    airline = FacadeBase.get_airline_by_id(id)
    serializer = AirlineCompanyModelSerializer(airline, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def get_airlines_by_parameters(name=None, country_id=None):
    airlines = FacadeBase.get_airline_by_parameters(name=None, country_id=None)
    serializer = AirlineCompanyModelSerializer(airlines, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_all_countries():
    countries = FacadeBase.get_all_countries()
    serializer = CountryModelSerializer(countries, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_country_by_id(id):
    country = FacadeBase.get_country_by_id(id)
    serializer = CountryModelSerializer(country, many=False)
    return Response(serializer.data)