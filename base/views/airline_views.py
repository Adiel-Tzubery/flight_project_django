from facads.airline_facade import AirlineFacade
from base.serializers import AirlineCompanyModelSerializer, FlightModelSerializer
from rest_framework import status

from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from auth.auth import group_required


@permission_classes([IsAuthenticated])
@api_view(['POST'])
@group_required('airline company')
def update_airline(request, airline_id,):
    """ getting the updated airline, serialize the new one and return the data. """

    try:
        updated_airline = AirlineFacade.update_airline(
            airline_id,
            username=request.data['username'],
            email=request.data['email'],
            password=request.data['password'],
            name=request.data['name'],
            country=request.data['country']
            )
        serializer = AirlineCompanyModelSerializer(updated_airline, many=False)
        return Response(serializer.data)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@permission_classes([IsAuthenticated])
@api_view(['POST'])
@group_required('airline company')
def add_flight(request):
    """ getting new flight, serialize it and return the data """

    try:
        flight = AirlineFacade.add_flight(
            airline_company=request.data['airline_company'],
            origin_country=request.data['origin_country'],
            destination_country=request.data['destination_country'],
            departure_time=request.data['departure_time'],
            landing_time=request.data['landing_time'],
            remaining_tickets=request.data['remaining_tickets'],
            price=request.data['price']
        )
        serializer = FlightModelSerializer(flight, many=False)
        return Response(serializer.data)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@permission_classes([IsAuthenticated])
@api_view(['POST'])
@group_required('airline company')
def update_flight(request, flight_id):
    """ getting the updated flight, serialize the new one and return the data. """

    try:
        updated_flight = AirlineFacade.update_flight(
            flight_id,
            departure_time=request.data['departure_time'],
            landing_time=request.data['landing_time'],
            remaining_tickets=request.data['remaining_tickets'],
            price=request.data['price']
            )
        serializer = FlightModelSerializer(updated_flight, many=False)
        return Response(serializer.data)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
@group_required('airline company')
def remove_flight(request, flight_id):
    """ remove flight view. """
    
    try:
        deleted_flight = AirlineFacade.remove_flight(flight_id)
        if deleted_flight:
            return Response({'message': 'Flight deleted successfully.'})
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_403_FORBIDDEN)
    

@permission_classes([IsAuthenticated])
@api_view(['GET'])
@group_required('airline company')
def get_my_flights(request, airline_id):
    """ getting list of airline's flights, serialize it and return the data. """

    try:
        flights = AirlineFacade.get_my_flights(airline_id)
        serializer = FlightModelSerializer(flights, many=len(flights) > 1)
        Response(serializer.data)
    except ObjectDoesNotExist as e:
        return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
    