from base.models import *
from dal.dal import DAL
from django.core.exceptions import ObjectDoesNotExist


class FacadeBase:

    @staticmethod
    def get_user_data(user_id):
        try:
            user_obj = DAL.get_by_id(User, user_id)
            role_data = DAL.get_role_data_by_user(user_obj)

            return user_obj, role_data
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist('User does not exists.')

    @staticmethod
    def get_all_flights():
        try:
            flights = DAL.get_all(Flight)
            return flights
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist('No flights found.')

    @staticmethod
    def get_flight_by_id(flight_id):
        try:
            flight = DAL.get_by_id(Flight, flight_id)
            return flight
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                f'Flight with id: {flight_id} does not exist.')

    @staticmethod
    def get_flights_by_parameters(origin_country, destination_country, date):
        try:
            flights = DAL.get_flights_by_parameters(
                origin_country, destination_country, date)
            return flights
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                'No flights found with the specified parameters.')

    @staticmethod
    def get_all_airlines():
        try:
            airlines = DAL.get_all(AirlineCompany)
            return airlines
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist('There are no airlines.')

    @staticmethod
    def get_airline_by_id(airline_id):
        try:
            airline = DAL.get_by_id(AirlineCompany, airline_id)
            return airline
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                f'There are no airline with id: {airline_id}.')

    @staticmethod
    def get_airline_by_parameters(name, country_id):
        """ return list of all the airlines or reduce it according to conditions, if there are any. """
        try:
            airline = DAL.get_airlines_by_parameters(name, country_id)
            return airline
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                'No airlines found with the specified parameters.')

    @staticmethod
    def get_all_countries():
        try:
            counties = DAL.get_all(Country)
            return counties
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist('There are no countries.')

    @staticmethod
    def get_country_by_id(country_id):
        try:
            country = DAL.get_by_id(Country, country_id)
            return country
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                f'There are no country with id: {country_id}.')
