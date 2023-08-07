from facads.customer_facade import CustomerFacade
from base.serializers import CustomerModelSerializer, TicketModelSerializer

from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework import status

from auth.auth import group_required

<<<<<<< HEAD
=======

>>>>>>> 67ead05e66aec98e01d0bd2b95b3906e5918d43f

@permission_classes([IsAuthenticated])
@api_view(['POST'])
@group_required('customer')
<<<<<<< HEAD
def update_customer(request):
    """ getting the updated customer, serialize the new user and return the data. """
    try:
        updated_customer = CustomerFacade.update_customer(
            customer_id=request.data['customer_id'],
=======
def update_customer(request, customer_id):
    """ getting the updated customer, serialize the new user and return the data. """
    try:
        updated_customer = CustomerFacade.update_customer(
            customer_id,
>>>>>>> 67ead05e66aec98e01d0bd2b95b3906e5918d43f
            username=request.data['username'],
            email=request.data['email'],
            password=request.data['password'],
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
            credit_card_no=request.data['credit_card_no'],
            phone_no=request.data['phone_no'],
            address=request.data['address'],
<<<<<<< HEAD
        )
=======
            )
>>>>>>> 67ead05e66aec98e01d0bd2b95b3906e5918d43f
        serializer = CustomerModelSerializer(updated_customer, many=False)
        return Response(serializer.data)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
<<<<<<< HEAD

=======
    
>>>>>>> 67ead05e66aec98e01d0bd2b95b3906e5918d43f

@permission_classes([IsAuthenticated])
@api_view(['POST'])
@group_required('customer')
<<<<<<< HEAD
def add_ticket(request):
    """ getting new ticket from the facade, serialize it and return the data """

    try:
        ticket = CustomerFacade.add_ticket(
            customer_id=request.data['customer_id'],
            flight_id=request.data['flight_id'])
=======
def add_ticket(request, customer_id):
    """ getting new ticket, serialize it and return the data """

    try:
        ticket = CustomerFacade.add_ticket(customer_id, flight_id=request.data('flight_id'))
>>>>>>> 67ead05e66aec98e01d0bd2b95b3906e5918d43f
        serializer = TicketModelSerializer(ticket, many=False)
        return Response(serializer.data)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
<<<<<<< HEAD

=======
    
>>>>>>> 67ead05e66aec98e01d0bd2b95b3906e5918d43f

@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
@group_required('customer')
<<<<<<< HEAD
def remove_ticket(request):
=======
def remove_ticket(request, ticket_id):
>>>>>>> 67ead05e66aec98e01d0bd2b95b3906e5918d43f
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
<<<<<<< HEAD
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
=======
def get_my_tickets(request, customer_id):
    """ getting list of customer's tickets, serialize it and return the data. """
    try:
        tickets = CustomerFacade.get_my_tickets(customer_id)
        serializer = TicketModelSerializer(tickets, many=len(tickets) > 1)
        return Response(serializer.data)
    except ObjectDoesNotExist as e:
        return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
>>>>>>> 67ead05e66aec98e01d0bd2b95b3906e5918d43f
