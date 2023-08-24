from base.models import *
from dal.dal import DAL
from django.core.exceptions import ObjectDoesNotExist


class FacadeBase:

    @staticmethod
    def get_user_data(user_id):
        """ return all user data according to it's id """
        try:
            user_obj = DAL.get_by_id(User, user_id)
            role_data = DAL.get_role_data_by_user(user_obj)

            return user_obj, role_data
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
    def get_flights_by_parameters(origin_country, destination_country, date):
        """ return list of all the flights or reduce it according to conditions, if there is any. """

        try:
            flights = DAL.get_flights_by_parameters(
                origin_country, destination_country, date)
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
