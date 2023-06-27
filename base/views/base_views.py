from facads.facade_base import FacadeBase
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from base.serializers import FlightModelSerializer, AirlineCompanyModelSerializer, CountryModelSerializer



@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_all_flights(request):
    try:
        flights = FacadeBase.get_all_flights()
        serializer = FlightModelSerializer(flights, many=True)
        return Response(serializer.data)
    except Exception:
        return Response({'message': 'There are no flights'}, status=status.HTTP_404_NOT_FOUND)



@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_flight_by_id(request, flight_id):
    try:
        flight = FacadeBase.get_flight_by_id(flight_id)
        serializer = FlightModelSerializer(flight, many=False)
        return Response(serializer.data)
    except Exception:
        raise Exception


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_flights_by_parameters(request, origin_country_id=None, destination_country_id=None, date=None):
    try:
        flights = FacadeBase.get_flights_by_parameters(origin_country_id=origin_country_id,
                                                        destination_country_id=destination_country_id,
                                                        date=date)
        serializer = FlightModelSerializer(flights, many=True) # what to do for cases where thee is 0/1 flights in the many=?
        return Response(serializer.data)
    except Exception:
        raise Exception


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_all_airlines(request):
    try:
        airlines = FacadeBase.get_all_airlines()
        serializer = AirlineCompanyModelSerializer(airlines, many=True)
        return Response(serializer.data)
    except Exception:
        raise Exception


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_airline_by_id(request, airline_id):
    try:
        airline = FacadeBase.get_airline_by_id(airline_id)
        serializer = AirlineCompanyModelSerializer(airline, many=False)
        return Response(serializer.data)
    except Exception:
        raise Exception


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_airlines_by_parameters(request, name=None, country_id=None):
    try:
        airlines = FacadeBase.get_airline_by_parameters(name=name, country_id=country_id)
        serializer = AirlineCompanyModelSerializer(airlines, many=True)
        return Response(serializer.data)
    except Exception:
        raise Exception


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_all_countries(request):
    try:
        countries = FacadeBase.get_all_countries()
        serializer = CountryModelSerializer(countries, many=True)
        return Response(serializer.data)
    except Exception:
        raise Exception

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_country_by_id(request, country_id):
    try:
        country = FacadeBase.get_country_by_id(country_id)
        serializer = CountryModelSerializer(country, many=False)
        return Response(serializer.data)
    except Exception:
        raise Exception
    

@csrf_exempt
@api_view(['POST'])
def log_out(request):
    try:
        refresh_token = request.data['refresh_token']
        OutstandingToken.objects.filter(token=refresh_token).delete()
        return Response(status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        raise Exception(f'{str(e)}')
        # return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)