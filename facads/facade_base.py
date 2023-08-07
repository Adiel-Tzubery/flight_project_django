from base.models import *
from dal.dal import DAL
from datetime import datetime
import pytz
from django.core.exceptions import ObjectDoesNotExist

# @@@@@@@@@@@@@@@@@@@@@@@@@ DON'T FORGET THE USER UPDATE METHOD, + ADD ONE TO ADMINISTRATOR @@@@@@@@@@@@@@@@@@@@@@@@@


class FacadeBase:

    @staticmethod
    def get_user_data(user_id):
        """ return all user data according to it's id """
        try:
<<<<<<< HEAD
            user_obj = DAL.get_by_id(User, user_id)
            role_data = DAL.get_role_data_by_user(user_obj)

            return user_obj, role_data
=======
            user_data = DAL.get_by_id(User, user_id)
            return user_data
>>>>>>> 67ead05e66aec98e01d0bd2b95b3906e5918d43f
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist('User does not exists.')

    @staticmethod
    def get_all_flights():
        """ return list of all the flights, if there are any. """

        try:
            flights = DAL.get_all(Flight)
            return flights
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist('No flights found.')

    @staticmethod
    def get_flight_by_id(flight_id):
        """ return a specific flight according to it's id.  """

        try:
            flight = DAL.get_by_id(Flight, flight_id)
            return flight
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                f'Flight with id: {flight_id} does not exist.')

    @staticmethod
    def get_flights_by_parameters(origin_country_id=None, destination_country_id=None, date=None):
        """ return list of all the flights or reduce it according to conditions, if there is any. """

        try:
            flights = DAL.get_flights_by_parameters(
                origin_country_id, destination_country_id, date)
            return flights
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                'No flights found with the specified parameters.')

    @staticmethod
    def get_all_airlines():
        """ return list of all the airlines, if there are any. """

        try:
            airlines = DAL.get_all(AirlineCompany)
            return airlines
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist('There are no airlines.')

    @staticmethod
    def get_airline_by_id(airline_id):
        """ return a specific airline according to it's id.  """

        try:
            airline = DAL.get_by_id(AirlineCompany, airline_id)
            return airline
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                f'There are no airline with id: {airline_id}.')

    @staticmethod
    def get_airline_by_parameters(name, country_id):
        """ return list of all the airlines or reduce it according to conditions, if there is any. """

        try:
            airline = DAL.get_airlines_by_parameters(name, country_id)
            return airline
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                'No airlines found with the specified parameters.')

    @staticmethod
    def get_all_countries():
        """ return list of all the airlines, if there are any. """

        try:
            counties = DAL.get_all(Country)
            return counties
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist('There are no countries.')

    @staticmethod
    def get_country_by_id(country_id):
        """ return a specific country according to it's id.  """

        try:
            country = DAL.get_by_id(Country, country_id)
            return country
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                f'There are no country with id: {country_id}.')

            # --------------------------------------------------------------------------------------------------------------------------#
            #                                           __________VALIDATIONS__________                                                #
            # --------------------------------------------------------------------------------------------------------------------------#


class FacadsValidator:

    """ class that contain all the facads validation checks. """

    @staticmethod
    def is_username_not_exists(username):
        """ check if the username taken """
<<<<<<< HEAD
        try:
            if DAL.get_user_by_username(username):
                # this wil be logger: ('username is taken, please try another one.')
                raise Exception(f'username: {username} is taken')
        except ObjectDoesNotExist:
            return True
        except Exception as e:
            raise Exception(f'error: {str(e)}')

    @staticmethod
    def is_email_not_exists(email):
        """ check if the email taken """
        try:
            if DAL.get_user_by_email(email):
                # this wil be logger: ('username is taken, please try another one.')
                raise Exception(f'email: {email} is taken')
        except ObjectDoesNotExist:
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
    def is_phone_not_exists(phone):
        " check if phone number taken "
        try:
            if DAL.get_customer_by_phone(phone):
                # this wil be logger: (f'phone number is taken, please try another one.')
                raise Exception(f'phone number {phone} is taken')
=======
        try:
            if DAL.get_user_by_username(username):
                # this wil be logger: ('username is taken, please try another one.')
                raise Exception(f'username: {username} is taken')
        except ObjectDoesNotExist:
            return True
        except Exception as e:
            raise Exception(f'error: {str(e)}')

    @staticmethod
    def is_email_not_exists(email):
        """ check if the email taken """
        try:
            if DAL.get_user_by_email(email):
                # this wil be logger: ('username is taken, please try another one.')
                raise Exception(f'email: {email} is taken')
        except ObjectDoesNotExist:        
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
    def is_phone_not_exists(phone):
        " check if phone number taken "
        try:
            if DAL.get_customer_by_phone(phone):
                # this wil be logger: (f'phone number is taken, please try another one.')
                raise Exception(f'phone number {phone} is taken')
        except ObjectDoesNotExist:
            return True
        except Exception as e:
            raise Exception(f'Error: {str(e)}.')

    @staticmethod
    def is_credit_not_exists(credit):
        """ check if credit card number taken """
        try:
            if DAL.get_customer_by_credit(credit):
                # this wil be logger: ('credit number is taken, pleas try another one.')
                raise Exception(f'credit card number {credit} taken')
        except ObjectDoesNotExist:
            return True
        except Exception as e:
            raise Exception(f'Error: {str(e)}.')
        
    @staticmethod
    def is_country_has_no_airline(country_id):
        try:
            if DAL.get_airlines_by_country_id(country_id):
                raise Exception('country cannot have more then one airline.')
>>>>>>> 67ead05e66aec98e01d0bd2b95b3906e5918d43f
        except ObjectDoesNotExist:
            return True
        except Exception as e:
            raise Exception(f'Error: {str(e)}.')

    @staticmethod
    def is_credit_not_exists(credit):
        """ check if credit card number taken """
        try:
            if DAL.get_customer_by_credit(credit):
                # this wil be logger: ('credit number is taken, pleas try another one.')
                raise Exception(f'credit card number {credit} taken')
        except ObjectDoesNotExist:
            return True
        except Exception as e:
            raise Exception(f'Error: {str(e)}.')

    @staticmethod
    def is_country_has_no_airline(country_id):
        try:
            if DAL.get_airlines_by_country_id(country_id):
                raise Exception('country cannot have more then one airline.')
        except ObjectDoesNotExist:
            return True
        except Exception as e:
            raise Exception(f'Error: {str(e)}.')

    @staticmethod
    def is_airline_clear_for_delete(airline_id):
        """ check if airline exists and have no flights. if do, the method return True. """

        try:  # check airline exists.
            airline_exists = DAL.get_by_id(AirlineCompany, airline_id)
            if airline_exists:
                # if airline have flights.
                flights = DAL.get_flights_by_airline_id(airline_id)
                if flights.exists():
                    return False
                return True  # if valid
            raise ObjectDoesNotExist(
                f'There are no airline with id: {airline_id}.')
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                f'There are no airline with id: {airline_id}.')

    @staticmethod
    def is_customer_clear_for_delete(customer_id):
        """ if customer has no tickets, it's ready to be deleted, in this case the method return True.  """

<<<<<<< HEAD
        customer_exists = DAL.get_by_id(Customer, customer_id)    
        try:    
            # if customer have tickets.
            if DAL.get_tickets_by_customer_id(customer_id):
                return False
        except: # if not valid
            return True


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
=======
        try:  # check customer exists.
            customer_exists = DAL.get_by_id(Customer, customer_id)
            if customer_exists:
                # if customer have tickets.
                tickets = DAL.get_tickets_by_customer_id(customer_id)
                if tickets.exists():
                    return False
                return True  # if valid
            raise ObjectDoesNotExist(
                f'There are no customer with id: {customer_id}.')
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                f'There are no customer with id: {customer_id}.')

    @staticmethod
    def is_flight_valid(flight_id, origin_country, destination_country, departure_time, landing_time, remaining_tickets, price):
        """ return true if all the flight parameters are valid and return True. """

        try:
            # check if flight took of already.
            old_flight = DAL.get_by_id(Flight, flight_id)
            if old_flight.departure_time < datetime.now():
                raise Exception(
                    'flight already took off and cannot be updated.')

            # data validations.
            if departure_time < datetime.now():
>>>>>>> 67ead05e66aec98e01d0bd2b95b3906e5918d43f
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
                    'one of origin/destination must be the airline country.')
            return True
        except Exception as e:
            raise Exception(f'Error: {str(e)}.')
<<<<<<< HEAD

    def is_flight_not_booked(customer_id, flight_id):
        tickets = DAL.get_tickets_by_customer_id(customer_id)
        for ticket in tickets:
            if ticket.flight.id == flight_id:
                return False
        return True
=======
>>>>>>> 67ead05e66aec98e01d0bd2b95b3906e5918d43f
