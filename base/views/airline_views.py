from facads.airline_facade import AirlineFacade
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from auth.auth import group_required
from base.serializers import AirlineCompanyModelSerializer, FlightModelSerializer


@permission_classes([IsAuthenticated])
@group_required('airline company')
@api_view(['POST'])
def update_airline(request, airline_id, **kwargs):
    try:
        updated_airline = AirlineFacade.update_airline(airline_id, kwargs)
        serializer = AirlineCompanyModelSerializer(updated_airline, many=False)
        return Response(serializer.data)
    except Exception:
        raise Exception
    

@permission_classes([IsAuthenticated])
@group_required('airline company')
@api_view(['POST'])
def add_flight(request, **kwargs):
    try:
        flight = AirlineFacade.add_flight(kwargs)
        serializer = FlightModelSerializer(flight, many=False)
        return Response(serializer.data)
    except Exception:
        raise Exception
    

@permission_classes([IsAuthenticated])
@group_required('airline company')
@api_view(['POST'])
def update_flight(request, flight_id, **kwargs):
    try:
        updated_flight = AirlineFacade.update_flight(flight_id, kwargs)
        serializer = FlightModelSerializer(updated_flight, many=False)
        return Response(serializer.data)
    except Exception:
        raise Exception
    

@permission_classes([IsAuthenticated])
@group_required('airline company')
@api_view(['DELETE'])
def remove_flight(request, flight_id):
    try:
        deleted_flight = AirlineFacade.remove_flight(flight_id)
        if deleted_flight:
            return Response({'message': 'Flight deleted successfully.'})
    except Exception:
        return Response({'message': 'Flight cannot be deleted.'}, status=409)
    

@permission_classes([IsAuthenticated])
@group_required('airline company')
@api_view(['GET'])
def get_my_flight(request, airline_id):
    try:
        flights = AirlineFacade.get_my_flights(airline_id)
        serializer = FlightModelSerializer(flights, many=False)
        Response(serializer.data)
    except  Exception:
        raise Exception
    