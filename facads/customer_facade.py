from .facads_validator import FacadsValidator
from .facade_base import FacadeBase
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password
from dal.dal import DAL
from base.models import Customer, Flight, Ticket, User
from datetime import datetime
import pytz


class CustomerFacade(FacadeBase):

    def update_customer(**kwargs):
        """ return updated user if the data passes validations. """
        customer = DAL.get_by_id(Customer, kwargs['customer_id'])

        try:  # consider possibility that not every fields are to update
            if customer.user.username != kwargs['username'] and FacadsValidator.is_username_not_exists(username=kwargs['username']) or customer.user.username == kwargs['username']:
                if customer.user.email != kwargs['email'] and FacadsValidator.is_email_not_exists(kwargs['email']) or customer.user.email == kwargs['email']:
                    if customer.phone_no != kwargs['phone_no'] and FacadsValidator.is_phone_not_exists(phone=kwargs['phone_no']) or customer.phone_no == kwargs['phone_no']:
                        if kwargs['credit_card_no'] != '' and FacadsValidator.is_credit_not_exists(credit=kwargs['credit_card_no']) or kwargs['credit_card_no'] == '':

                            # if there is new password, set it, else set it to original
                            if kwargs['new_password'] != '':
                                if check_password(kwargs['password'], customer.user.password):
                                    kwargs['password'] = kwargs['new_password']
                                else:
                                    raise Exception('old password not match')
                            else:
                                kwargs['password'] = customer.user.password


                            # if not provided, set the credit to original
                            if kwargs['credit_card_no'] == '':
                                kwargs['credit_card_no'] = customer.credit_card_no

                            # update user
                            id = customer.user.id  # to user id
                            DAL.update(
                                User,
                                id,
                                username=kwargs['username'],
                                email=kwargs['email'],
                            )

                            # update customer
                            id = kwargs['customer_id']  # to customer id
                            updated_customer = DAL.update(
                                Customer,
                                id,
                                password=kwargs['password'],
                                first_name=kwargs['first_name'],
                                last_name=kwargs['last_name'],
                                credit_card_no=kwargs['credit_card_no'],
                                phone_no=kwargs['phone_no'],
                                address=kwargs['address'])
                            return updated_customer
        except Exception as e:
            raise Exception(f'{str(e)}')

    def add_ticket(customer_id, flight_id):
        # check if there are available tickets + if flight took off
        try:
            flight = DAL.get_by_id(Flight, flight_id)
            if flight.departure_time < datetime.now(pytz.UTC):
                raise Exception('Flight departed')
            if flight.remaining_tickets < 1:
                raise Exception('There are no tickets available')

            if FacadsValidator.is_flight_not_booked(customer_id, flight_id):
                # getting the actual instance
                customer = DAL.get_by_id(Customer, customer_id)

                # creating ticket
                ticket = DAL.create(Ticket, customer=customer, flight=flight)

                # update remaining_tickets
                remaining_tickets = flight.remaining_tickets - 1
                flight = DAL.update(Flight, flight_id,
                                    remaining_tickets=remaining_tickets)

                return ticket
            else:
                raise Exception(f'you already booked this flight')
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f'No Flight found with id {flight_id}')
        except Exception as e:
            raise Exception(f'{str(e)}')

    def remove_ticket(ticket_id):
        """ delete and return ticket if it's on time. """
        try:
            ticket = DAL.get_by_id(Ticket, ticket_id)
            if ticket.flight.departure_time < datetime.now(pytz.UTC):
                raise Exception('Cannot cancel ticket for past flight')

            # update remaining_tickets
            remaining_tickets = ticket.flight.remaining_tickets + 1
            DAL.update(
                Flight,
                ticket.flight.id,
                remaining_tickets=remaining_tickets)
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
