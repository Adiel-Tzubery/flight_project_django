from facads.customer_facade import CustomerFacade
from base.serializers import CustomerModelSerializer, TicketModelSerializer

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


from auth.auth import group_required


@permission_classes([IsAuthenticated])
@api_view(['PUT'])
@group_required('customer')
def update_customer(request):
    try:
        updated_customer = CustomerFacade.update_customer(
            customer_id=request.data['customer_id'],
            username=request.data['username'],
            email=request.data['email'],
            password=request.data['password'],
            new_password=request.data['new_password'],
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
            credit_card_no=request.data['credit_card_no'],
            phone_no=request.data['phone_no'],
            address=request.data['address'],
        )
        serializer = CustomerModelSerializer(updated_customer, many=False)
        return Response(serializer.data)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
@group_required('customer')
def add_ticket(request):
    """ customer bout a ticked """

    try:
        ticket = CustomerFacade.add_ticket(
            customer_id=request.data['customer_id'],
            flight_id=request.data['flight_id'])
        serializer = TicketModelSerializer(ticket, many=False)
        return Response(serializer.data)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
@group_required('customer')
def remove_ticket(request):
    try:
        deleted_ticket = CustomerFacade.remove_ticket(
            ticket_id=request.query_params['ticket_id'])
        if deleted_ticket:
            return Response({'message': 'Ticket deleted successfully.'})
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_403_FORBIDDEN)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
@group_required('customer')
def get_my_tickets(request):
    try:
        tickets = CustomerFacade.get_my_tickets(
            customer_id=request.query_params['customer_id'])
        serializer = TicketModelSerializer(tickets, many=True)
        return Response(serializer.data)
    except ObjectDoesNotExist as e:
        return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
