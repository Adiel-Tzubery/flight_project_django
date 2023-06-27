from facads.administrator_facade import AdministratorFacade
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from auth.auth import group_required
from base.serializers import CustomerModelSerializer, AirlineCompanyModelSerializer, AdministratorModelSerializer



@permission_classes([IsAuthenticated])
@group_required('administrator')
@api_view(['GET'])
def get_all_customers(request):
    try:
        customers = AdministratorFacade.get_all_customers()
        serializer = CustomerModelSerializer(customers, many=True)
        return Response(serializer.data)
    except Exception:
        raise Exception


@permission_classes([IsAuthenticated])
@group_required('administrator')
@api_view(['POST'])
def add_airline(request, **kwargs):
    try:
        airline = AdministratorFacade.add_airline(kwargs)
        serializer = AirlineCompanyModelSerializer(airline, many=False)
        return Response(serializer.data)
    except Exception:
        raise Exception


@permission_classes([IsAuthenticated])
@group_required('administrator')
@api_view(['POST'])
def add_customer(request, **kwargs):
    try:
        customer = AdministratorFacade.add_customer(kwargs)
        serializer = CustomerModelSerializer(customer, many=False)
        return Response(serializer.data)
    except Exception:
        raise Exception


@permission_classes([IsAuthenticated])
@group_required('administrator')
@api_view(['POST'])
def add_administrator(request, **kwargs):
    try:
        administrator = AdministratorFacade.add_administrator(kwargs)
        serializer = AdministratorModelSerializer(administrator, many=False)
        return Response(serializer.data)
    
    except Exception:
        raise Exception


@permission_classes([IsAuthenticated])
@group_required('administrator')
@api_view(['DELETE'])
def remove_airline(request, airline_id):
    try:
        deleted_airline = AdministratorFacade.remove_airline(airline_id)
        if deleted_airline:
            return Response({'message': 'Airline deleted successfully.'})
    except Exception:
        return Response({'message': 'Airline cannot be deleted.'}, status=409)


@permission_classes([IsAuthenticated])
@group_required('administrator')
@api_view(['DELETE'])
def remove_customer(request, customer_id):
    try:
        deleted_customer = AdministratorFacade.remove_customer(customer_id)
        if deleted_customer:
            return Response({'message': 'Customer deleted successfully.'})
    except Exception:
        return Response({'message': 'Customer cannot be deleted.'}, status=409)


@permission_classes([IsAuthenticated])
@group_required('administrator')
@api_view(['DELETE'])
def remove_administrator(request, administrator_id):
    try:
        deleted_admin = AdministratorFacade.remove_administrator(administrator_id)
        if deleted_admin:
            return Response({'message': 'Administrator deleted successfully.'})
    except Exception:
        return Response({'message': 'Administrator cannot be deleted.'}, status=409)