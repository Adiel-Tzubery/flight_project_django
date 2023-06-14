from base.models import *
from dal.dal import DAL
from datetime import datetime


class FacadeBase:
    
    @staticmethod
    def get_all_flights():
        try:
            flights = DAL.get_all(Flight)
            return flights
        except Exception:
            raise Exception


    @staticmethod
    def get_flight_by_id(flight_id):
        try:
            flight = DAL.get_by_id(Flight, flight_id)
            return flight
        except Exception:
            raise Exception


    @staticmethod
    def get_flights_by_parameters(origin_country_id=None, destination_country_id=None, date=None):
        try:
            flights = DAL.get_flights_by_parameters(origin_country_id=None, destination_country_id=None, date=None)
            return flights
        except Exception:
            raise Exception


    @staticmethod
    def get_all_airlines():
        try:
            airlines = DAL.get_all(AirlineCompany)
            return airlines
        except Exception:
            raise Exception

    @staticmethod
    def get_airline_by_id(airline_id):
        try:
            airline = DAL.get_by_id(AirlineCompany, airline_id)
            return airline
        except Exception:
            raise Exception


    @staticmethod    
    def get_airline_by_parameters(name, country_id):
        try:
            airline = DAL.get_airlines_by_parameters(name, country_id)
            return airline
        except Exception:
            raise Exception


    @staticmethod
    def get_all_countries():
        try:
            counties = DAL.get_all(Country)
            return counties
        except Exception:
            raise Exception


    @staticmethod
    def get_country_by_id(country_id):
        try:
            country = DAL.get_by_id(Country, country_id)
            return country
        except  Exception:
            raise Exception


    @staticmethod
    def log_out():
        pass


class FacadsValidator:

    @staticmethod
    def is_username_or_email_exists(username, email):
        """ check if there username or emile are taken """
        try: 
            username_exist = DAL.get_user_by_username(username)
            if username_exist:
                raise Exception('username is taken, please try another one')
            email_exists = DAL.get_user_by_emil(email)
            if email_exists.exists():
                raise Exception('email is taken, please try another one')
            return False
        except Exception:
            raise Exception


    @staticmethod    
    def is_phone_or_credit_exists(phone, credit):
        " check if credit phone/card number are exists "
        try:
            phone_exists = DAL.get_customer_by_phone(phone)
            if phone_exists:
                raise Exception(f'phone number is taken, please try another one')
            credit_exists = DAL.get_customer_by_credit(credit)
            if credit_exists:
                raise Exception('credit number is taken, pleas try another one')
            return False
        except:
            raise Exception


    @staticmethod
    def is_airline_clear_for_delete(airline_id):
        """ check if airline exists and have no flights """
        try: # check if airline exists.
            airline_exists = DAL.get_by_id(AirlineCompany, airline_id)
            if airline_exists:
                # if airline have flights.
                flights = DAL.get_flights_by_airline_id(airline_id)
                if flights.exists():
                    raise Exception('airline cannot be deleted while having flight/s')
                try: # if exist and have no flights, deleted airline.
                    return True
                except Exception:
                    raise Exception
            raise Exception('airline does not exists')
        except Exception:
            raise Exception
        

    @staticmethod
    def is_customer_clear_for_delete(customer_id):
        try: # check if customer exists.
            customer_exists = DAL.get_by_id(Customer, customer_id)
            if customer_exists:
                # if customer have tickets.
                tickets = DAL.get_tickets_by_customer_id(customer_id)
                if tickets.exists():
                    raise Exception('customer cannot be deleted while having ticket/s')
                try: # if exists and have no tickets, delete customer.
                    return True
                except Exception:
                    raise Exception
            raise Exception('customer does not exist')
        except Exception:
            raise Exception
        

    @staticmethod
    def is_flight_valid(origin_country, destination_country, departure_time, landing_time, remaining_tickets, price):
        try:
            if departure_time < datetime.now():
                raise Exception('flight date cannot be in the past')
            if remaining_tickets < 0:
                raise Exception('minimum tickets: 0')
            if price < 0:
                raise Exception('minimum price: 0$')
            if landing_time > departure_time:
                raise Exception('departure time must be before landing time')
            if origin_country == destination_country:
                raise Exception('flight must be international')
            return True
        except Exception:
            raise Exception