from .facade_base import FacadeBase, FacadsValidator
from django.core.exceptions import ObjectDoesNotExist
from dal.dal import DAL
from base.models import Customer, Flight, Ticket
from datetime import datetime


class CustomerFacade(FacadeBase):

    def update_customer(customer_id, **kwargs):
        try:  # data validations
            if not FacadsValidator.is_username_or_email_exists(username=kwargs['username'], email=kwargs['email']):
                if FacadsValidator.is_phone_or_credit_exists(phone=kwargs['phone_no'], credit=kwargs['credit_card_no']):
                    updated_customer = DAL.update(Customer, customer_id,
                                                    username=kwargs['username'],
                                                    email=kwargs['email'],
                                                    password=kwargs['password'],
                                                    profile_piq=kwargs['profile_piq'],
                                                    first_name=kwargs['first_name'],
                                                    last_name=kwargs['last_name'],
                                                    credit_card_no=kwargs['credit_card_no'],
                                                    phone_no=kwargs['phone_no'],
                                                    address=kwargs['address'])
                    return updated_customer
        except Exception as e:
            raise Exception(f'{str(e)}')

    def add_ticket(customer_id, flight_id):
        try:  # check for available tickets
            flight = DAL.get_by_id(Ticket, flight_id)
            if flight.departure_time < datetime.no():
                raise Exception('Flight departed')
            if flight.remaining_tickets < 1:
                raise Exception('There are no tickets available')
            # update remaining_tickets
            remaining_tickets = flight.remaining_tickets - 1  
            flight = DAL.update(Flight, flight_id, remaining_tickets=remaining_tickets)
            # creating ticket
            ticket = DAL.create(Ticket, customer=customer_id, flight=flight_id)
            return ticket
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f'No Flight found with id {flight_id}')
        except Exception as e:
            raise Exception(f'{str(e)}')

    def remove_ticket(ticket_id):
        try:
            ticket = DAL.get_by_id(Ticket, ticket_id)
            if ticket.flight.departure_time < datetime.now():
                raise Exception('Cannot cancel ticket for past flight')
            # update remaining_tickets
            remaining_tickets = ticket.flight.remaining_tickets + 1
            DAL.update(Flight,ticket.flight.id, remaining_tickets=remaining_tickets)
            deleted_ticket = DAL.remove(Ticket, ticket_id)
            return deleted_ticket
        except Exception as e:
            raise Exception(f'{str(e)}')

    def get_my_tickets(customer_id):
        try:
            tickets = DAL.get_tickets_by_customer_id(customer_id)
            return tickets
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist('Customer have no tickets.')
