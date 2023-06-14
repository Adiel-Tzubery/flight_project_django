from facads.administrator_facade import AdministratorFacade
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.serializers import CustomerModelSerializer, AirlineCompanyModelSerializer, AdministratorModelSerializer



@api_view(['GET'])
def get_all_customers(request):
    try:
        customers = AdministratorFacade.get_all_customers(request)
        serializer = CustomerModelSerializer(customers, many=True)
        return Response(serializer.data)
    except Exception:
        raise Exception


@api_view(['POST'])
def add_airline(request, **kwargs):
    try:
        airline = AdministratorFacade.add_airline(kwargs)
        serializer = AirlineCompanyModelSerializer(airline, many=False)
        return Response(serializer.data)
    except Exception:
        raise Exception


@api_view(['POST'])
def add_customer(request, **kwargs):
    try:
        customer = AdministratorFacade.add_customer(kwargs)
        serializer = CustomerModelSerializer(customer, many=False)
        return Response(serializer.data)
    except Exception:
        raise Exception


@api_view(['POST'])
def add_administrator(request, **kwargs):
    try:
        administrator = AdministratorFacade.add_administrator(kwargs)
        serializer = AdministratorModelSerializer(administrator, many=False)
        return Response(serializer.data)
    except Exception:
        raise Exception


@api_view(['DELETE'])
def remove_airline(request, airline_id):
    try:



@api_view(['DELETE'])
def remove_customer(request, customer_id):
    try:
        AdministratorFacade.remove_customer(customer_id):
        return Response({'message': 'Customer deleted successfully.'})
    except Exception:
        return Response({'message': 'Customer cannot be deleted.'}, status=409)



@api_view(['DELETE'])
def remove_administrator(request, administrator_id):
    pass