from base.models import *
from dal.dal import DAL



class FacadeBase:

    def get_all_flights():
        DAL.get_all(Flight)


    def get_flight_by_id(id):
        DAL.get_by_id(Flight, id)


    def get_flights_by_parameters(origin_country_id=None, destination_country_id=None, date=None):
        DAL.get_flights_by_parameters(origin_country_id=None, destination_country_id=None, date=None)


    def get_all_airlines():
        DAL.get_all(AirlineCompany)


    def get_airline_by_id(id):
        DAL.get_by_id(AirlineCompany, id)

    @staticmethod
    def get_airline_by_parameters(name, country_id):
        DAL.get_airlines_by_parameters(name, country_id)


    def get_all_countries():
        DAL.get_all(Country)


    def get_country_by_id(id):
        DAL.get_by_id(Country, id)