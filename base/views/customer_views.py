from facads.customer_facade import CustomerFacade
from base.serializers import CustomerModelSerializer, TicketModelSerializer

from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework import status

from auth.auth import group_required


@permission_classes([IsAuthenticated])
@api_view(['POST'])
@group_required('customer')
def update_customer(request):
    """ getting the updated customer, serialize the new user and return the data. """
    try:
        updated_customer = CustomerFacade.update_customer(
            customer_id=request.data['customer_id'],
            username=request.data['username'],
            email=request.data['email'],
            password=request.data['password'],
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
    """ getting new ticket from the facade, serialize it and return the data """

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
    """ remove ticket view. """

    try:
        deleted_ticket = CustomerFacade.remove_ticket(
            ticket_id=request.data['ticket_id'])
        if deleted_ticket:
            return Response({'message': 'Ticket deleted successfully.'})
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_403_FORBIDDEN)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
@group_required('customer')
def get_my_tickets(request):
    """ getting list of customer's tickets, serialize it and return the data. """
    try:
        # customer_id = Customer.objects.filter(
        #     user=request.user.id).first().user

        tickets = CustomerFacade.get_my_tickets(
            customer_id=request.query_params['customer_id'])
        serializer = TicketModelSerializer(tickets, many=len(tickets) > 1)
        return Response(serializer.data)
    except ObjectDoesNotExist as e:
        return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
