from facads.facade_base import FacadeBase
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from base.serializers import FlightModelSerializer, AirlineCompanyModelSerializer, CountryModelSerializer, UserModelSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_data(request):
    try:
        user_obj, role_data = FacadeBase.get_user_data(request.user.id)
        serializer = UserModelSerializer(user_obj, many=False)

        # Merge between serializer.data and role_data objs
        merged_obj = {}

        merged_obj.update(role_data)
        merged_obj.update(serializer.data)

        # the merged object that includes both objs
        return Response(merged_obj)
    except ObjectDoesNotExist as e:
        return Response({'message': str(e)}, status=status.HTTP_100_CONTINUE)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_flights(request):
    """ getting list of all the flights, serialize it and return it's data. """

    try:
        flights = FacadeBase.get_all_flights()
        serializer = FlightModelSerializer(flights, many=True)
        return Response(serializer.data)
    except ObjectDoesNotExist as e:
        return Response({'message': str(e)}, status=status.HTTP_100_CONTINUE)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_flight_by_id(request):
    """ getting the flight, serialize it and return it's data. """

    try:
        flight = FacadeBase.get_flight_by_id(
            flight_id=request.query_params['flight_id'])
        serializer = FlightModelSerializer(flight, many=False)
        return Response(serializer.data)
    except ObjectDoesNotExist as e:
        return Response({'message:': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([AllowAny])
@api_view(['GET'])
def get_flights_by_parameters(request):
    """ getting list of all the flights, serialize it and return it's data. """
    try:
        if request.method == 'GET':
            origin_country = request.query_params['origin_country']
            destination_country = request.query_params['destination_country']
            date = request.query_params['departure_time']

            flights = FacadeBase.get_flights_by_parameters(
                origin_country, destination_country, date)

            if flights:
                serializer = FlightModelSerializer(flights, many=True)
                return Response(serializer.data)
    except ObjectDoesNotExist as e:
        return Response({'message': str(e)}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_all_airlines(request):
    """ getting list of all the airlines, serialize it and return it's data. """

    try:
        airlines = FacadeBase.get_all_airlines()
        serializer = AirlineCompanyModelSerializer(
            airlines, many=True)
        return Response(serializer.data)
    except ObjectDoesNotExist as e:
        return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_airline_by_id(request):
    """ getting the airline, serialize it and return it's data. """

    try:
        airline = FacadeBase.get_airline_by_id(
            airline_id=request.data['airline_id'])
        serializer = AirlineCompanyModelSerializer(airline, many=False)
        return Response(serializer.data)
    except ObjectDoesNotExist as e:
        return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_airlines_by_parameters(request):
    """ getting list of all the airlines, serialize it and return it's data. """

    try:
        name = request.GET.get("name")
        country_id = request.GET.get("country_id")
        airlines = FacadeBase.get_airline_by_parameters(
            name=name, country_id=country_id)
        serializer = AirlineCompanyModelSerializer(
            airlines, many=True)
        return Response(serializer.data)
    except ObjectDoesNotExist as e:
        return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_all_countries(request):
    """ getting list of all the countries, serialize it and return it's data. """

    try:
        countries = FacadeBase.get_all_countries()
        serializer = CountryModelSerializer(
            countries, many=True)
        return Response(serializer.data)
    except ObjectDoesNotExist as e:
        return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_country_by_id(request):
    """ getting the country, serialize it and return it's data. """

    try:
        country = FacadeBase.get_country_by_id(
            country_id=request.data['country_id'])
        serializer = CountryModelSerializer(country, many=False)
        return Response(serializer.data)
    except ObjectDoesNotExist as e:
        return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def log_out(request):
    """ logout view. """
    try:
        refresh_token = request.data['refresh_token']
        OutstandingToken.objects.filter(token=refresh_token).delete()
        return Response(status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({'massage': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
