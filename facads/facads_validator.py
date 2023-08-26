from base.models import *
from dal.dal import DAL
from datetime import datetime
import pytz
from django.core.exceptions import ObjectDoesNotExist


class FacadsValidator:

    """ class that contain all the facads validation checks. """

    #                                       @@@@@@@@@@@@@@@@@@@_______ USER VALIDATIONS _______@@@@@@@@@@@@@@@@@@@

    @staticmethod
    def is_username_not_exists(username):
        try:
            if DAL.get_user_by_username(username):
                raise Exception(f'username: {username} is taken')
        except ObjectDoesNotExist:
            return True
        except Exception as e:
            raise Exception(f'error: {str(e)}')

    @staticmethod
    def is_email_not_exists(email):
        try:
            if DAL.get_user_by_email(email):
                raise Exception(f'email: {email} is taken')
        except ObjectDoesNotExist:
            return True
        except Exception as e:
            raise Exception(f'error: {str(e)}')

    #                                       @@@@@@@@@@@@@@@@@@@_______ CUSTOMER VALIDATIONS _______@@@@@@@@@@@@@@@@@@@

    @staticmethod
    def is_phone_not_exists(phone):
        try:
            if DAL.get_customer_by_phone(phone):
                raise Exception(f'phone number {phone} is taken')
        except ObjectDoesNotExist:
            return True
        except Exception as e:
            raise Exception(f'Error: {str(e)}.')

    @staticmethod
    def is_credit_not_exists(credit):
        try:
            if DAL.get_customer_by_credit(credit):
                raise Exception(f'credit card number {credit} taken')
        except ObjectDoesNotExist:
            return True
        except Exception as e:
            raise Exception(f'Error: {str(e)}.')

    @staticmethod
    def is_customer_clear_for_delete(customer_id):
        """ delete only if customer has no active tickets """

        try:
            tickets = DAL.get_tickets_by_customer_id(customer_id)
            # check for an active flight
            for ticket in tickets:
                flight = DAL.get_by_id(Flight, ticket.flight.id)
                if flight.landing_time >= datetime.now(pytz.UTC):
                    return False
            return True
        except:  # if customer haven't got any tickets.
            return True

    #                                       @@@@@@@@@@@@@@@@@@@_______ AIRLINE COMPANY VALIDATIONS _______@@@@@@@@@@@@@@@@@@@

    @staticmethod
    def validate_airline_before_creation(name, country_id):
        try:
            if FacadsValidator.is_airline_name_not_exists(name):
                if FacadsValidator.is_country_has_no_airline(country_id):
                    return True
        except Exception as e:
            raise Exception(f'error: {str(e)}')

    @staticmethod
    def is_airline_name_not_exists(name):
        try:
            if DAL.get_airline_by_name(name):
                raise Exception(f'name: {name} is taken')
        except ObjectDoesNotExist:
            return True
        except Exception as e:
            raise Exception(f'error: {str(e)}')

    @staticmethod
    def is_country_has_no_airline(country_id):
        try:
            if DAL.get_airlines_by_country_id(country_id):
                raise Exception('country already have an airline.')
        except ObjectDoesNotExist:
            return True
        except Exception as e:
            raise Exception(f'Error: {str(e)}')

    @staticmethod
    def is_airline_clear_for_delete(airline_id):
        """ delete only if airline have active flight/s."""
        try:
            flights = DAL.get_flights_by_airline_id(airline_id)
            if flights.exists():
                for flight in flights:
                    if flight.landing_time >= datetime.now(pytz.UTC):
                        return False

                # all the flights has ended
                return True
        # if valid
        except ObjectDoesNotExist as e:
            return True

    #                                       @@@@@@@@@@@@@@@@@@@_______ FLIGHT VALIDATIONS _______@@@@@@@@@@@@@@@@@@@

    @staticmethod
    def is_flight_valid(**kwargs):
        """ return true if all the flight parameters are valid and return True. """
        try:

            # flight airline
            airline = DAL.get_by_id(AirlineCompany, kwargs['airline_company'])

            try:
                # when updating:
                # check if flight took of already.
                if kwargs['flight_id']:
                    old_flight = DAL.get_by_id(Flight, kwargs['flight_id'])
                    if old_flight.departure_time < datetime.now(pytz.UTC):
                        raise Exception(
                            'flight already took off and cannot be updated.')
            except KeyError:
                pass
            except Exception:
                raise Exception(f'Error: {str(e)}.')

            # data validations.
            # pytz.UTC get the current datetime with UTC timezone
            if kwargs['departure_time'] < datetime.now(pytz.UTC):
                raise Exception('flight date cannot be in the past.')
            if kwargs['remaining_tickets'] < 0:
                raise Exception('minimum tickets: 0.')
            if kwargs['price'] < 0:
                raise Exception('minimum price: 0$.')
            if kwargs['landing_time'] < kwargs['departure_time']:
                raise Exception('departure time must be before landing time.')
            if kwargs['origin_country'] == kwargs['destination_country']:
                raise Exception('flight must be international.')
            if kwargs['origin_country'] != airline.country.id and kwargs['destination_country'] != airline.country.id:
                raise Exception(
                    'one of origin/destination must be the airline country')
            return True
        except Exception as e:
            raise Exception(f'Error: {str(e)}.')

    def is_flight_not_booked(customer_id, flight_id):
        try:
            tickets = DAL.get_tickets_by_customer_id(customer_id)
            for ticket in tickets:
                if ticket.flight.id == flight_id:
                    return False
            return True
        # if user has no tickets
        except ObjectDoesNotExist:
            return True
