from django.core.exceptions import ObjectDoesNotExist, ValidationError
from base.models import AirlineCompany, Flight, Customer, Ticket, User, Country, UserRole



class DAL:
    """ class DAL for direct communication with the data base.
    the first 6 method are global to all the models and the rest is model specific """
    
    @staticmethod
    def get_by_id(model, id):
        """ get an instance of a model by his id """
        try:
            instance =  model.objects.get(pk=id)
            return instance
        except model.DoesNotExist:
            raise ObjectDoesNotExist(f'No {model.__name__} found with id {id}')
        except Exception as e:
            raise Exception(f'Error occurred while retrieving instance of model: {model.__name__}, error: {str(e)}')


    @staticmethod
    def get_all(model):
        """ get all instances of a model """
        try:
            instances = model.objects.all()
            if not instances.exists():
                raise ObjectDoesNotExist(f'No instances found for model: {model.__name__}.')
            return instances
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f'No instances found for model: {model.__name__}.')
        except Exception as e:
            raise Exception(f'Error occurred while retrieving instances of model: {model.__name}, error: {str(e)}.')
        
    

    @staticmethod
    def create(model,**kwargs):
        """ add an instance to a model """
        try:
            if 'administrator' in kwargs.values():
                obj = model.objects.create_superuser(**kwargs)
            elif 'customer' in kwargs.values() or 'airline company' in kwargs.values():
                obj = model.objects.create_user(**kwargs)
                obj.user_role = UserRole.objects.get(role_name='customer')
                obj.save()
            else:
                obj = model.objects.create(**kwargs)
                obj.user_role = UserRole.objects.get(role_name='customer')
                obj.save()
            return obj
        except Exception as e:
            raise Exception(f'Error occurred while creating instance of model: {model.__name__}, error: {str(e)}.')
        

    @staticmethod
    def add_all(model, items):
        """ add multiple instances of a model at once """
        try:
            return model.objects.bulk_create(items)
        except ValidationError as e:
            raise Exception(f'Error bulk creating model: {model.__name__}, error: {str(e)} ')
        

    @staticmethod
    def update(model, id, **kwargs):
        """ update an instance of a model """
        try:
            instance = DAL.get_by_id(model, id)
            for key, value in kwargs.items():
                # handle only the fields that need to be change
                if hasattr(instance, key):
                    setattr(instance, key,  value)
            instance.save()
            return instance
        except model.DoesNotExist:
            raise ObjectDoesNotExist(f'No {model.__name__} found with id {id}.')
        except Exception as e:
            raise Exception(f'Error while updating {model.__name__}, error: {str(e)}.')


    @staticmethod
    def remove(model, id):
        """ remove an instance of a model """
        try:
            instance = DAL.get_by_id(model, id)
            instance.delete()
            return instance
        except model.DoesNotExist:
            raise ObjectDoesNotExist(f'No {model.__name__} found with id {id}.')
    

    @staticmethod
    def get_customer_by_phone(phone_no):
        try:
            customer = Customer.objects.filter(phone_no=phone_no)
            if not customer.exists():
                raise ObjectDoesNotExist(f'No customer found with phone number: {phone_no}.')
            return customer
        except Customer.DoesNotExist:
            raise ObjectDoesNotExist(f'No customer found with phone number: {phone_no}.')
        

    @staticmethod
    def get_customer_by_credit(credit):
        try:
            customer = Customer.objects.filter(credit_card_no=credit)
            if not customer.exists():
                raise ObjectDoesNotExist(f'No customer found with credit number: {credit}.')
            return customer
        except Customer.DoesNotExist:
            raise ObjectDoesNotExist(f'No customer found with credit number: {credit}.')
        

    @staticmethod
    def get_airlines_by_country_id(id):
        """ get all the airlines of a country if there is any """
        country = DAL.get_by_id('Country', id)
        try:
            airlines = AirlineCompany.objects.filter(country__id=id).all()
            if not airlines.exists():
                raise ObjectDoesNotExist(f'There are no airlines in {country.name}.')
            return airlines
        except Country.DoesNotExist:
            raise ObjectDoesNotExist(f'No country found with id {id}.')
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f'There are no airlines in {country.name}.')


    @staticmethod
    def get_flights_by_origin_country_id(id):
        """ get all the flights that departure from a country """
        origin_country = DAL.get_by_id('Country', id)
        try:
            flights = Flight.objects.filter(origin_country__id=id).all()
            if not flights:
                raise ObjectDoesNotExist(f'There are no flights from {origin_country.name}.')
            return flights
        except Country.DoesNotExist:
            raise ObjectDoesNotExist(f'No country found with id {id}.')
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f'There are no flights from {origin_country.name}.')
        

    @staticmethod
    def get_flights_by_destination_country_id(id):
        """ gel all the flights that landing in a country """
        destination_country = DAL.get_by_id('Country', id)
        try:
            flights = Flight.objects.filter(destination_country__id=id).all()
            if not flights.exists():
                raise ObjectDoesNotExist(f'There are no flights to {destination_country.name}.')
            return flights
        except Country.DoesNotExist:
            raise ObjectDoesNotExist(f'No country found with id {id}.')
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f'There are no flights to {destination_country.name}.')
        

    @staticmethod
    def get_flights_by_departure_date(date):
        """ get all the flights that departure at a searched date """
        try:
            flights = Flight.objects.filter(departure_time=date)
            if not flights.exists():
                raise ObjectDoesNotExist(f'There are no flights on {date}.')
            return flights
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f'There are no flights on {date}.')
        

    @staticmethod
    def get_flights_by_landing_date(date):
        """ get all the flights that landing at a searched date """
        try:
            flights = Flight.objects.filter(landing_time=date)
            if not flights.exists():
                raise ObjectDoesNotExist(f'There are no flights landing on {date}.')
            return flights
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f'There are no flights landing on {date}.')
        
    
    @staticmethod
    def get_flights_by_customer(customer):
        try:
            tickets = Ticket.objects.filter(customer=customer)
            if not tickets.exists():
                raise ObjectDoesNotExist(f"{customer.first_name} hasn't booked any flights.")
            flights = [ticket.flight for ticket in tickets]
            return flights
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f"{customer.first_name} hasn't booked any flights.")
        

    @staticmethod
    def get_tickets_by_flight_id(flight_id):
        try:
            tickets = Ticket.objects.filter(flight=flight_id)
            if tickets.exists():
                raise ObjectDoesNotExist('Flight has not sold any tickets')
            return tickets
        except ObjectDoesNotExist:
                raise ObjectDoesNotExist('Flight has not sold any tickets')


    #@@@@@@@@@@@@@@@@@@@@@ MODEL'S METHODS @@@@@@@@@@@@@@@@@@@@@#

    @staticmethod
    def get_flights_by_parameters(origin_country_id=None, destination_country_id=None, date=None):
        try:
            flights = Flight.get_flights_by_parameters(origin_country_id=None, destination_country_id=None, date=None)
            if not flights.exists():
                raise ObjectDoesNotExist('No flights found with the specified parameters.')
            return flights
        except Flight.DoesNotExist:
            raise ObjectDoesNotExist('No flights found with the specified parameters.')


    @staticmethod
    def get_airlines_by_parameters(name=None, country_id=None):
        try:
            airlines = AirlineCompany.get_airlines_by_parameters(name, country_id)
            if not airlines.exists():
                raise ObjectDoesNotExist('No airlines found with the specified parameters.')
            return airlines
        except AirlineCompany.DoesNotExist:
            raise ObjectDoesNotExist('No airlines found with the specified parameters.')

    @staticmethod
    def get_flights_by_airline_id(airline_id):
        try:
            flights = Flight.get_flights_by_airline_id(airline_id)
            if not flights.exists():
                raise ObjectDoesNotExist('This airline has no flights.')
            return flights
        except Flight.DoesNotExist:
                raise ObjectDoesNotExist('This airline has no flights.')
            

    @staticmethod
    def get_arrival_flights(country_id):
        try:
            flights = Flight.get_arrival_flights(country_id)
            if not flights.exists():
                raise ObjectDoesNotExist('There are no flights to this country.')
            return flights
        except Flight.DoesNotExist:
            raise ObjectDoesNotExist('There are no flights to this country.')


    @staticmethod
    def get_departure_flights(country_id):
        try:
            flights = Flight.get_departure_flights(country_id)
            if not flights.exists():
                raise ObjectDoesNotExist('There are no flights from this country.')
            return flights
        except Flight.DoesNotExist:
            raise ObjectDoesNotExist('There are no flights from this country.')


    @staticmethod
    def get_tickets_by_customer_id(customer_id):
        try:
            tickets = Ticket.get_tickets_by_customer_id(customer_id)
            if not tickets.exists():
                raise ObjectDoesNotExist('Customer have no tickets.')
            return tickets
        except Ticket.DoesNotExist:
            raise ObjectDoesNotExist('Customer have no tickets.')


    @staticmethod
    def get_user_by_username(username):
        try:
            user = User.get_user_by_username(username)
            return user
        except User.DoesNotExist:
            raise ObjectDoesNotExist(f'There is no user with username: {username}.')


    @staticmethod
    def get_user_by_email(email):
        try:
            user = User.get_user_by_email(email)
            return user
        except User.DoesNotExist:
            raise ObjectDoesNotExist(f'There is no user with email: {email}.')


    @staticmethod
    def get_customer_by_username(username):
        try:
            customer = Customer.get_customer_by_username(username)
            return customer
        except Customer.DoesNotExist:
            raise ObjectDoesNotExist(f'There is no customer with username: {username}.')


    @staticmethod
    def get_airline_by_username(username):
        try:
            airline = AirlineCompany.get_airline_by_username(username)
            return airline
        except AirlineCompany.DoesNotExist:
            raise ObjectDoesNotExist(f'There is no airline with username: {username}.')