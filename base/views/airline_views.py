from facads.airline_facade import AirlineFacade
from base.serializers import AirlineCompanyModelSerializer, FlightModelSerializer
from rest_framework import status

from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from auth.auth import group_required


@permission_classes([IsAuthenticated])
@api_view(['PUT'])
@group_required('airline company')
def update_airline(request):
    try:
        updated_airline = AirlineFacade.update_airline(
            airline_id=request.data['airline_id'],
            username=request.data['username'],
            email=request.data['email'],
            password=request.data['password'],
            new_password=request.data['new_password'],
            name=request.data['name'],
        )
        serializer = AirlineCompanyModelSerializer(updated_airline, many=False)
        return Response(serializer.data)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
@group_required('airline company')
def add_flight(request):
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
@api_view(['PUT'])
@group_required('airline company')
def update_flight(request):
    try:
        updated_flight = AirlineFacade.update_flight(
            airline_company=request.data['airline_company'],
            flight_id=request.data['flight_id'],
            origin_country=request.data['origin_country'],
            destination_country=request.data['destination_country'],
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
def remove_flight(request):
    try:
        deleted_flight = AirlineFacade.remove_flight(
            flight_id=request.query_params['flight_id'])
        if deleted_flight:
            return Response({'message': 'Flight deleted successfully.'})
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_403_FORBIDDEN)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
@group_required('airline company')
def get_my_flights(request):
    try:
        flights = AirlineFacade.get_my_flights(
            airline_id=request.query_params['airline_id'])
        serializer = FlightModelSerializer(flights, many=True)
        return Response(serializer.data)
    except ObjectDoesNotExist as e:
        return Response({'message': str(e)}, status=status.HTTP_100_CONTINUE)
