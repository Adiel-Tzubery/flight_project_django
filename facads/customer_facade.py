from .facade_base import FacadeBase, FacadsValidator
from django.core.exceptions import ObjectDoesNotExist
from dal.dal import DAL
from base.models import Customer, Flight, Ticket
from datetime import datetime



class CustomerFacade(FacadeBase):


    def update_customer(customer_id, **kwargs):
        username = kwargs['username']
        email = kwargs['email']
        password = kwargs['password']
        profile_piq = kwargs['profile_piq']
        first_name = kwargs['first_name']
        last_name = kwargs['last_name']
        credit_card_no = kwargs['credit_card_no']
        phone_no = kwargs['phone_no']
        address = kwargs['address']
        try: # data validations
            if not FacadsValidator.is_username_or_email_exists(username=username, email=email):
                if FacadsValidator.is_phone_or_credit_exists(phone=phone_no, credit=credit_card_no):
                    updated_customer = DAL.update(Customer, customer_id,
                                                username=username,
                                                email=email,
                                                password=password,
                                                profile_piq=profile_piq,
                                                first_name=first_name,
                                                last_name=last_name,
                                                credit_card_no=credit_card_no,
                                                phone_no=phone_no,
                                                address=address)
                    return updated_customer
        except Exception:
            raise Exception


    def add_ticket(customer_id, flight_id):
        try: # check for available tickets
            flight = DAL.get_by_id(Ticket, flight_id)
            if flight.departure_time < datetime.now():
                raise Exception('Flight departed')
            if flight.remaining_tickets < 1:
                raise Exception('There is no tickets remain')
            flight.remaining_tickets -= 1 # do need DAL method?
            ticket = DAL.create(Ticket, customer=customer_id, flight=flight_id)
            return ticket
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f'No Flight found with id {flight_id}')
        except Exception:
            raise Exception
            


    def remove_ticket(ticket_id):
        try:
            ticket = DAL.get_by_id(Ticket, ticket_id)
            if ticket.flight.departure_time < datetime.now():
                raise Exception('Cannot cancel ticket for past flight')
            ticket.flight.remaining_tickets += 1 # do need DAL method?
            deleted_ticket = DAL.remove(Ticket, ticket_id)
            return deleted_ticket
        except Exception:
            raise Exception

            



    def get_my_tickets(customer_id):
        try:
            tickets = DAL.get_tickets_by_customer_id(customer_id)
            return tickets
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f'No tickets found for customer')