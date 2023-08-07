from facads.administrator_facade import AdministratorFacade
from auth.auth import group_required
from base.serializers import CustomerModelSerializer, AirlineCompanyModelSerializer, AdministratorModelSerializer
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


@permission_classes([IsAuthenticated])
@api_view(['GET'])
@group_required('administrator')
def get_all_customers(request):
    """ getting list of all the customers, serialize it and return it's data. """

    try:
        customers = AdministratorFacade.get_all_customers()
        serializer = CustomerModelSerializer(
            customers, many=len(customers) > 1)
        return Response(serializer.data)
    except Exception:
        raise Exception


@permission_classes([IsAuthenticated])
@group_required('administrator')
def add_airline(request):
    """ get new airline, serialize it and return it's data. """

    try:
        airline = AdministratorFacade.add_airline(
            username=request.data['username'],
            email=request.data['email'],
            password=request.data['password'],
            name=request.data['name'],
            country=request.data['country'],
            user_role=request.data['user_role']
        )
        serializer = AirlineCompanyModelSerializer(airline, many=False)
        return Response(serializer.data)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
@group_required('administrator')
def add_customer(request):
    """ get new airline, serialize it and return it's data. """

    try:
        customer = AdministratorFacade.add_customer(
            username=request.data['username'],
            email=request.data['email'],
            password=request.data['password'],
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
            credit_card_no=request.data['credit_card_no'],
            phone_no=request.data['phone_no'],
            address=request.data['address'],
            user_role=request.data['user_role'],
        )
        serializer = CustomerModelSerializer(customer, many=False)
        return Response(serializer.data)
    except Exception as e:
        return Response({'Error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
@group_required('administrator')
def add_administrator(request):
    """ get new airline, serialize it and return it's data. """

    try:
        administrator = AdministratorFacade.add_administrator(
            username=request.data['username'],
            email=request.data['email'],
            password=request.data['password'],
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
            user_role=request.data['user_role'],
        )
        serializer = AdministratorModelSerializer(administrator, many=False)
        return Response(serializer.data)
    except Exception as e:
        return Response({'Error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
@group_required('administrator')
def remove_airline(request, airline_id):
    """ remove airline view. """

    try:
        deleted_airline = AdministratorFacade.remove_airline(airline_id)
        if deleted_airline:
            return Response({'message': 'Airline deleted successfully.'})
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_403_FORBIDDEN)


@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
@group_required('administrator')
@api_view(['DELETE'])
def remove_customer(request, customer_id):
    try:
        deleted_customer = AdministratorFacade.remove_customer(
            customer_id=request.query_params['customer_id'])
        if deleted_customer:
            return Response({'message': 'Customer deleted successfully.'})
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_403_FORBIDDEN)


@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
@group_required('administrator')
@api_view(['DELETE'])
def remove_administrator(request, administrator_id):
    try:
        deleted_admin = AdministratorFacade.remove_administrator(administrator_id)
        if deleted_admin:
            return Response({'message': 'Administrator deleted successfully.'})
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_403_FORBIDDEN)
