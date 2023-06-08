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


    def log_out():
        pass


class FacadsValidator:
    def is_username_or_email_exists(username, email):
        """ check if there username or emile are taken """
        try: 
            username_exist = DAL.get_user_by_username(username)
            if username_exist:
                raise Exception('username is taken, try another one')
            email_exists = DAL.get_user_by_emil(email)
            if email_exists.exists():
                raise Exception('email is taken, try another one')
            return True
        except Exception:
            raise Exception
        

    def is_airline_clear_for_delete(airline):
        """ check if airline exists and have no flights """
        try: # check if airline exists.
            airline_exists = DAL.get_by_id(AirlineCompany, airline.id)
            if airline_exists:
                # if airline have flights.
                flights = DAL.get_flights_by_airline_id(airline.id)
                if flights.exists():
                    raise Exception('airline cannot be deleted while having flight/s')
                try: # if exist and have no flights, deleted airline.
                    return True
                except Exception:
                    raise Exception
            raise Exception('airline does not exists')
        except Exception:
            raise Exception
        

    def is_customer_clear_for_delete(customer):
        try: # check if customer exists.
            customer_exists = DAL.get_by_id(Customer, customer.id)
            if customer_exists:
                # if customer have tickets.
                tickets = DAL.get_tickets_by_customer_id(customer.id)
                if tickets.exists():
                    raise Exception('customer cannot be deleted while having ticket/s')
                try: # if exists and have no tickets, delete customer.
                    return True
                except Exception:
                    raise Exception
            raise Exception('customer does not exist')
        except Exception:
            raise Exception