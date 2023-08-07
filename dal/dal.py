from django.core.exceptions import ObjectDoesNotExist, ValidationError
from base.models import Administrator, AirlineCompany, Flight, Customer, Ticket, User, Country, UserRole


class DAL:
    """ class DAL for direct communication with the data base. """

    #        @@@@@@@@@@@@@_____first 6 method are global to all the models and the rest is model specific_____@@@@@@@@@@@@@

    @staticmethod
    def get_by_id(model, id):
        """ return instance according to it's id. """

        try:  # get and return the instance.
            instance = model.objects.get(pk=id)
            return instance
        except model.DoesNotExist:  # if the instance does not exist.
            raise ObjectDoesNotExist(f'No {model.__name__} found with id {id}')
        except Exception as e:  # any other error.
            raise Exception(
                f'Error occurred while retrieving instance of model: {model.__name__}, error: {str(e)}')

    @staticmethod
    def get_all(model):
        """ return list of all the instances of a requested model. """

        try:  # get and return the list.
            instances = model.objects.all()
            if not instances.exists():  # if there isn't even one instance of the model.
                raise ObjectDoesNotExist(
                    f'No instances found for model: {model.__name__}.')
            return instances
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                f'No instances found for model: {model.__name__}.')
        except Exception as e:  # any other error.
            raise Exception(
                f'Error occurred while retrieving instances of model: {model.__name}, error: {str(e)}.')

    @staticmethod
    def create(model, **kwargs):
        """ create and return a new instance of a requested model. """

        # if instance is user/superuser/other, preform different creation method.
        try:
            if 'administrator' in kwargs.values():
                obj = model.objects.create_superuser(**kwargs)
            elif 'customer' in kwargs.values() or 'airline company' in kwargs.values():
                obj = model.objects.create_user(**kwargs)
            else:
                obj = model.objects.create(**kwargs)
                obj.save()  # saving the instance.
            return obj
        except Exception as e:  # in case of an error.
            raise Exception(
                f'Error occurred while creating instance of model: {model.__name__}, error: {str(e)}.')

    @staticmethod
    def add_all(model, items):
        """ create and return multiple instances of a model at once. """

        try:
            instances = model.objects.bulk_create(items)
            return instances
        except ValidationError as e:
            raise Exception(
                f'Error bulk creating model: {model.__name__}, error: {str(e)} ')

    @staticmethod
    def update(model, id, **kwargs):
        """ update and return an instance of a requested model. """

        # @@@@@@@@@ handle case of kwargs comes with keys with empty values. @@@@@@@@@ 

        try:
            instance = DAL.get_by_id(model, id)
            for key, value in kwargs.items():
                # handle only the fields that need to be change
                if hasattr(instance, key):
                    setattr(instance, key,  value)
            # save and return updated instance.
            instance.save()
            return instance
        # error handling if instance does not exists or any other error.
        except model.DoesNotExist:
            raise ObjectDoesNotExist(
                f'No {model.__name__} found with id {id}.')
        except Exception as e:
            raise Exception(
                f'Error while updating {model.__name__}, error: {str(e)}.')

    @staticmethod
    def remove(model, id):
        """ remove and return an instance of a requested model """

        try:  # get, delete and return the instance.
            instance = DAL.get_by_id(model, id)
            instance.delete()
            return instance
<<<<<<< HEAD
        except model.DoesNotExist:  # if instance does not exists before deleting.
            raise ObjectDoesNotExist(
                f'No {model.__name__} found with id {id}.')

    # ------------------------------------------------------------------------------------------------------------------------------------

    #                                        _____@@@@@@@@@______ MODEL'S METHODS  DAL _____@@@@@@@@@_____

    @staticmethod
    def get_flights_by_parameters(origin_country_id=None, destination_country_id=None, date=None):
        """ return list of all the flights or reduce it according to conditions, if there is any. """

        try:  # get and return the flights.
            flights = Flight.get_flights_by_parameters(
                origin_country_id=None, destination_country_id=None, date=None)
            if not flights.exists():  # if there are no flights.
                raise ObjectDoesNotExist(
                    'No flights found with the specified parameters.')
            return flights
        except Flight.DoesNotExist:
            raise ObjectDoesNotExist(
                'No flights found with the specified parameters.')

    @staticmethod
    def get_airlines_by_parameters(name=None, country_id=None):
        """ return list of all the airlines or reduce it according to conditions, if there is any. """

        try:  # get and return the airlines.
            airlines = AirlineCompany.get_airlines_by_parameters(
                name, country_id)
            if not airlines.exists():  # if there are no airlines.
                raise ObjectDoesNotExist(
                    'No airlines found with the specified parameters.')
            return airlines
        except AirlineCompany.DoesNotExist:
            raise ObjectDoesNotExist(
                'No airlines found with the specified parameters.')

    @staticmethod
    def get_flights_by_airline_id(airline_id):
        """ return all flights of specific airline according to it's id. """

        try:  # get and return the flights.
            flights = Flight.get_flights_by_airline_id(airline_id)
            if not flights.exists():  # if there are no flights.
                raise ObjectDoesNotExist('This airline has no flights.')
            return flights
        except Flight.DoesNotExist:
            raise ObjectDoesNotExist('This airline has no flights.')

    @staticmethod
    def get_arrival_flights(country_id):
        """ return list of all flights that are arriving in the next 12 hours to specific country. """

        try:  # get and return the flights.
            flights = Flight.get_arrival_flights(country_id)
            if not flights.exists():  # if there are no flights.
                raise ObjectDoesNotExist(
                    'There are no flights to this country.')
            return flights
        except Flight.DoesNotExist:
            raise ObjectDoesNotExist('There are no flights to this country.')

    @staticmethod
    def get_departure_flights(country_id):
        """ return list of all the flights that are departure in the next 12 hours from specific country. """

        try:  # get and return the flights.
            flights = Flight.get_departure_flights(country_id)
            if not flights.exists():  # if there are no flights.
                raise ObjectDoesNotExist(
                    'There are no flights from this country.')
            return flights
        except Flight.DoesNotExist:
            raise ObjectDoesNotExist('There are no flights from this country.')

    @staticmethod
    def get_tickets_by_customer_id(customer_id):
        """ return list of all the customer's tickets. """

        try:  # get and return the tickets.
            tickets = Ticket.get_tickets_by_customer_id(customer_id)
            if not tickets:  # if there are no tickets.
                raise ObjectDoesNotExist('Customer have no tickets.')
            return tickets
        except Ticket.DoesNotExist:
            raise ObjectDoesNotExist('Customer have no tickets.')

    @staticmethod
    def get_user_by_username(username):
        """ return user according to it's username. """

        try:  # get and return the user.
            user = User.get_user_by_username(username)
            return user
        except User.DoesNotExist:  # if user does not exists.
            raise ObjectDoesNotExist(
                f'There is no user with username: {username}.')

    @staticmethod
    def get_user_by_email(email):
        """ return user according to it's email. """

        try:  # get and return the user.
            user = User.get_user_by_email(email)
            return user
        except User.DoesNotExist:  # if user does not exists.
            raise ObjectDoesNotExist(f'There is no user with email: {email}.')

    @staticmethod
    def get_customer_by_username(username):
        """ return customer according to it's user's username. """

        try:  # get and return the customer.
            customer = Customer.get_customer_by_username(username)
            return customer
        except Customer.DoesNotExist:  # if customer does not exists.
            raise ObjectDoesNotExist(
                f'There is no customer with username: {username}.')

    @staticmethod
    def get_airline_by_username(username):
        """ return airline according to it's user's username. """

        try:  # get and return the airline.
            airline = AirlineCompany.get_airline_by_username(username)
            return airline
        except AirlineCompany.DoesNotExist:  # if airline does not exists.
            raise ObjectDoesNotExist(
                f'There is no airline with username: {username}.')

    @staticmethod
    def get_airline_by_name(name):
        """ return airline according to it's name. """

        try:
            airline = AirlineCompany.get_airline_by_name(name)
            return airline
        except AirlineCompany.DoesNotExist:
            raise ObjectDoesNotExist(
                f'Airline with name {name} does not exists.')

    # ------------------------------------------------------------------------------------------------------------------------------------

    #                                        _____@@@@@@@@@______ ADDITIONAL DAL _____@@@@@@@@@_____
=======
        except model.DoesNotExist: # if instance does not exists before deleting.
            raise ObjectDoesNotExist(f'No {model.__name__} found with id {id}.')
    
    #------------------------------------------------------------------------------------------------------------------------------------
>>>>>>> 67ead05e66aec98e01d0bd2b95b3906e5918d43f

    @staticmethod
    def get_customer_by_phone(phone_no):
        """  get and return customer according to it's phone number.  """

        try:  # get and return.
            customer = Customer.objects.filter(phone_no=phone_no).first()
            if not customer:  # in case customer does not exists.
                raise ObjectDoesNotExist(
                    f'No customer found with phone number: {phone_no}.')
            return customer
        except Customer.DoesNotExist:
            raise ObjectDoesNotExist(
                f'No customer found with phone number: {phone_no}.')

    @staticmethod
    def get_customer_by_credit(credit):
        """ get and return customer according to it's credit number. """

        try:  # get and return.
            customer = Customer.objects.filter(credit_card_no=credit).first()
            if not customer:  # in case customer does not exists.
                raise ObjectDoesNotExist(
                    f'No customer found with credit number: {credit}.')
            return customer
        except Customer.DoesNotExist:
            raise ObjectDoesNotExist(
                f'No customer found with credit number: {credit}.')

    @staticmethod
    def get_airlines_by_country_id(id):
        """ return list of airlines from a country, if there is any. according to it's id. """

        # get the country.
        country = DAL.get_by_id(Country, id)
        try:  # check for airlines and return.
            airlines = AirlineCompany.objects.filter(country__id=id)
            if not airlines.exists():  # in case there is no airlines in the country.
                raise ObjectDoesNotExist(
                    f'There are no airlines in {country.name}.')
            return airlines
        except Country.DoesNotExist:  # in case that the country does not exists.
            raise ObjectDoesNotExist(f'No country found with id {id}.')
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                f'There are no airlines in {country.name}.')

    @staticmethod
    def get_flights_by_origin_country_id(id):
        """ return list of flights that departure from a country according to the country's id. """

        # get the country.
        origin_country = DAL.get_by_id('Country', id)
        try:  # check for flights and return.
            flights = Flight.objects.filter(origin_country__id=id)
            if not flights.exists():  # in case there is no flights.
                raise ObjectDoesNotExist(
                    f'There are no flights from {origin_country.name}.')
            return flights
        except Country.DoesNotExist:  # in case that the country does not exists.
            raise ObjectDoesNotExist(f'No country found with id {id}.')
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                f'There are no flights from {origin_country.name}.')

    @staticmethod
    def get_flights_by_destination_country_id(id):
        """ return list of the flights that arriving for a country according to the country's id. """

        # get the country.
        destination_country = DAL.get_by_id('Country', id)
        try:  # check for flights and return.
            flights = Flight.objects.filter(destination_country__id=id)
            if not flights.exists():  # in case there is no flights.
                raise ObjectDoesNotExist(
                    f'There are no flights to {destination_country.name}.')
            return flights
        except Country.DoesNotExist:  # in case that the country does not exists.
            raise ObjectDoesNotExist(f'No country found with id {id}.')
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                f'There are no flights to {destination_country.name}.')

    @staticmethod
    def get_flights_by_departure_date(date):
        """ return list of the flights that departure at a searched date. """

        try:  # check for flights and return.
            flights = Flight.objects.filter(departure_time=date)
            if not flights.exists():  # in case there is no flights.
                raise ObjectDoesNotExist(f'There are no flights on {date}.')
            return flights
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f'There are no flights on {date}.')

    @staticmethod
    def get_flights_by_landing_date(date):
        """ return list of the flights that arriving at a searched date. """

        try:  # check for flights and return.
            flights = Flight.objects.filter(landing_time=date)
            if not flights.exists():  # in case there is no flights.
                raise ObjectDoesNotExist(
                    f'There are no flights landing on {date}.')
            return flights
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                f'There are no flights landing on {date}.')

    @staticmethod
    def get_flights_by_customer(customer):
        """ return list of flights that customer bought ticket for. """

        try:  # get list of all the customer's tickets.
            tickets = Ticket.objects.filter(customer=customer)
            if not tickets.exists():  # in case that customer does not bought any tickets.
                raise ObjectDoesNotExist(
                    f"{customer.first_name} hasn't booked any flights.")
            # extract the flights from the tickets.
            flights = [ticket.flight for ticket in tickets]
            return flights
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                f"{customer.first_name} hasn't booked any flights.")

    @staticmethod
    def get_tickets_by_flight_id(flight_id):
        """ return list of all the tickets that sold for a specific flight. """

        try:
            tickets = Ticket.objects.filter(flight=flight_id)
            if tickets.exists():  # in case the flight hasn't sold any tickets.
                raise ObjectDoesNotExist(
                    'This flight have sold Tickets: cannot be canceled.')
            return tickets
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                'This flight have sold Tickets: cannot be canceled.')

    @staticmethod
    def get_country_by_name(name):
        try:
            country = Country.objects.filter(name=name).first()
            if not country:
                raise ObjectDoesNotExist
            return country
        except Country.DoesNotExist:
            raise ObjectDoesNotExist(
                f'Country with name {name} does not exists.')

    @staticmethod
    def get_role_data_by_user(user: object) -> object:
        """ get info to redux according the user role. """

        match user.user_role.role_name:
            case "administrator":
                admin_role_data = Administrator.objects.filter(
                    user=user).first()

                return {
                    "first_name": admin_role_data.first_name,
                    "last_name":  admin_role_data.last_name,
                    "administrator_id": admin_role_data.id
                }

            case "customer":
                customer_role_data = Customer.objects.filter(user=user).first()

                return {
                    "first_name": customer_role_data.first_name,
                    "last_name":  customer_role_data.last_name,
                    "phone_no": customer_role_data.phone_no,
                    "address": customer_role_data.address,
                    "customer_id": customer_role_data.id
                }

            case "airline company":
                airline_role_data = AirlineCompany.objects.filter(
                    user=user).first()

<<<<<<< HEAD
                return {
                    "name": airline_role_data.name,
                    "country":  airline_role_data.country.name,
                    "airline_id": airline_role_data.id
                }
=======

    @staticmethod
    def get_departure_flights(country_id):
        """ return list of all the flights that are departure in the next 12 hours from specific country. """

        try: # get and return the flights.
            flights = Flight.get_departure_flights(country_id)
            if not flights.exists(): # if there are no flights.
                raise ObjectDoesNotExist('There are no flights from this country.')
            return flights
        except Flight.DoesNotExist:
            raise ObjectDoesNotExist('There are no flights from this country.')


    @staticmethod
    def get_tickets_by_customer_id(customer_id):
        """ return list of all the customer's tickets. """

        try: # get and return the tickets.
            tickets = Ticket.get_tickets_by_customer_id(customer_id)
            if not tickets.exists(): # if there are no tickets.
                raise ObjectDoesNotExist('Customer have no tickets.')
            return tickets
        except Ticket.DoesNotExist:
            raise ObjectDoesNotExist('Customer have no tickets.')


    @staticmethod
    def get_user_by_username(username):
        """ return user according to it's username. """

        try: # get and return the user.
            user = User.get_user_by_username(username)
            return user
        except User.DoesNotExist: # if user does not exists.
            raise ObjectDoesNotExist(f'There is no user with username: {username}.')


    @staticmethod
    def get_user_by_email(email):
        """ return user according to it's email. """

        try: # get and return the user.
            user = User.get_user_by_email(email)
            return user
        except User.DoesNotExist: # if user does not exists.
            raise ObjectDoesNotExist(f'There is no user with email: {email}.')


    @staticmethod
    def get_customer_by_username(username):
        """ return customer according to it's user's username. """

        try: # get and return the customer.
            customer = Customer.get_customer_by_username(username)
            return customer
        except Customer.DoesNotExist: # if customer does not exists.
            raise ObjectDoesNotExist(f'There is no customer with username: {username}.')


    @staticmethod
    def get_airline_by_username(username):
        """ return airline according to it's user's username. """

        try: # get and return the airline.
            airline = AirlineCompany.get_airline_by_username(username)
            return airline
        except AirlineCompany.DoesNotExist: # if airline does not exists.
            raise ObjectDoesNotExist(f'There is no airline with username: {username}.')
        
    
    @staticmethod
    def get_airline_by_name(name):
        """ return airline according to it's name. """

        try:
            airline = AirlineCompany.get_airline_by_name(name)
            return airline
        except AirlineCompany.DoesNotExist:
            raise ObjectDoesNotExist(f'Airline with name {name} does not exists.')
>>>>>>> 67ead05e66aec98e01d0bd2b95b3906e5918d43f
