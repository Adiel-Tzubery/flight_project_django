from facads.customer_facade import CustomerFacade
from rest_framework.decorators import api_view
from rest_framework.response import Response
from auth.auth import group_required
from django.contrib.auth.decorators import login_required
from base.serializers import CustomerModelSerializer, TicketModelSerializer


@login_required
@group_required('customer')
@api_view(['POST'])
def update_customer(customer_id, **kwargs):
    try:
        updated_customer = CustomerFacade.update_customer(customer_id, kwargs)
        serializer = CustomerModelSerializer(updated_customer, many=False)
        return Response(serializer.data)
    except Exception:
        raise Exception
    

@login_required
@group_required('customer')
@api_view(['POST'])
def add_ticket(customer_id, flight_id):
    try:
        ticket = CustomerFacade.add_ticket(customer_id, flight_id)
        serializer = TicketModelSerializer(ticket, many=False)
        return Response(serializer.data)
    except Exception:
        raise Exception
    

@login_required
@group_required('customer')
@api_view(['DELETE'])
def remove_ticket(ticket_id):
    try:
        deleted_ticket = CustomerFacade.remove_ticket(ticket_id)
        if deleted_ticket:
            return Response({'message': 'Ticket deleted successfully.'})
    except Exception:
        return Response({'message': 'Ticket cannot be deleted.'}, status=409)


@login_required
@group_required('customer')
@api_view(['GET'])
def get_my_tickets(customer_id):
    try:
        tickets = CustomerFacade.get_my_tickets(customer_id)
        serializer = TicketModelSerializer(tickets, many=True)
        return Response(serializer.data)
    except Exception:
        raise Exception