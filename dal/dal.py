from django.core.exceptions import ObjectDoesNotExist, ValidationError
from base.models import Administrator, AirlineCompany, Flight, Customer, Ticket, User, Country
from datetime import datetime, time

from django.contrib.auth.hashers import check_password


class DAL:
    """ class DAL for direct communication with the data base. """

    #                                      @@@@@@@@@@@@@_____first 6 method are global to all the models _____@@@@@@@@@@@@@

    @staticmethod
    def get_by_id(model, id):
        try:
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

        try:
            instances = model.objects.all()
            if not instances.exists():  # if there isn't even one instance of the model.
                raise ObjectDoesNotExist(
                    f'No instances found for model: {model.__name__}.')
            return instances
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                f'No instances found for model: {model.__name__}.')
        except Exception as e:
            raise Exception(
                f'Error occurred while retrieving instances of model: {model.__name}, error: {str(e)}.')

    @staticmethod
    def create(model, **kwargs):
        # if instance is user/superuser/other, preform different creation method.
        try:
            if 'user_role' in kwargs.keys() and 'administrator' in kwargs.values():
                obj = model.objects.create_superuser(**kwargs)
            elif 'user_role' in kwargs.keys() and 'customer' in kwargs.values() or 'airline company' in kwargs.values():
                obj = model.objects.create_user(**kwargs)
            else:
                obj = model.objects.create(**kwargs)
                obj.save()  # saving the instance.
            return obj
        except Exception as e:
            raise Exception(
                f'Error occurred while creating instance of model: {model.__name__}, error: {str(e)}.')

    @staticmethod
    def add_all(model, items):
        try:
            instances = model.objects.bulk_create(items)
            return instances
        except ValidationError as e:
            raise Exception(
                f'Error bulk creating model: {model.__name__}, error: {str(e)} ')

    @staticmethod
    def update(model, id, **kwargs):
        try:
            instance = DAL.get_by_id(model, id)
            for key, value in kwargs.items():
                # handle only the fields that need to be change.
                if key == 'password':
                    # in different 'if' ( and not in 'and' ) statement to avoid the else case.
                    # only change password if the value is different from the existing password.
                    if not check_password(value, instance.user.password):
                        instance.user.set_password(value)
                        instance.user.save()
                        print(check_password(instance.user.password, value))
                else:
                    hasattr(instance, key)
                    setattr(instance, key,  value)
            instance.save()
            return instance
        except model.DoesNotExist:
            raise ObjectDoesNotExist(
                f'No {model.__name__} found with id {id}.')
        except Exception as e:
            raise Exception(
                f'Error while updating {model.__name__}, error: {str(e)}.')

    @staticmethod
    def remove(model, id):
        try:
            instance = DAL.get_by_id(model, id)
            instance.delete()
            return instance
        except model.DoesNotExist:  # if instance does not exists before deleting.
            raise ObjectDoesNotExist(
                f'No {model.__name__} found with id {id}.')

    # ------------------------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------

    #                                        _____@@@@@@@@@______ MODEL'S METHODS  DAL _____@@@@@@@@@_____

    @staticmethod
    def get_flights_by_parameters(origin_country=None, destination_country=None, date=None):
        """ return list of all the flights or reduce it according to conditions, if there are any. """
        try:
            origin_country_id = None
            destination_country_id = None
            date_time = None
            if origin_country:
                origin_country_id = Country.objects.get(name=origin_country)
            if destination_country:
                destination_country_id = Country.objects.get(
                    name=destination_country)
            if date:
                date = datetime.strptime(date, '%Y-%m-%d').date()
                date_time = datetime.combine(date, time.min)

            flights = Flight.get_flights_by_parameters(
                origin_country_id, destination_country_id, date_time)
            return flights
        except Flight.DoesNotExist:
            raise ObjectDoesNotExist(
                'No flights found with the specified parameters.')

    @staticmethod
    def get_airlines_by_parameters(name=None, country_id=None):
        """ return list of all the airlines or reduce it according to conditions, if there is any. """

        try:
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
        try:
            flights = Flight.get_flights_by_airline_id(airline_id)
            if not flights.exists():  # if there are no flights.
                raise ObjectDoesNotExist('This airline has no flights.')
            return flights
        except Flight.DoesNotExist:
            raise ObjectDoesNotExist('This airline has no flights.')

    @staticmethod
    def get_arrival_flights(country_id):
        """ return list of all flights that are arriving up to the next 12 hours to specific country. """

        try:
            flights = Flight.get_arrival_flights(country_id)
            if not flights.exists():  # if there are no flights.
                raise ObjectDoesNotExist(
                    'There are no flights to this country.')
            return flights
        except Flight.DoesNotExist:
            raise ObjectDoesNotExist('There are no flights to this country.')

    @staticmethod
    def get_departure_flights(country_id):
        """ return list of all the flights that are departure up to  the next 12 hours from specific country. """

        try:
            flights = Flight.get_departure_flights(country_id)
            if not flights.exists():  # if there are no flights.
                raise ObjectDoesNotExist(
                    'There are no flights from this country.')
            return flights
        except Flight.DoesNotExist:
            raise ObjectDoesNotExist('There are no flights from this country.')

    @staticmethod
    def get_tickets_by_customer_id(customer_id):
        try:
            tickets = Ticket.get_tickets_by_customer_id(customer_id)
            if not tickets:
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
            raise ObjectDoesNotExist(
                f'There is no user with username: {username}.')

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
            raise ObjectDoesNotExist(
                f'There is no customer with username: {username}.')

    @staticmethod
    def get_airline_by_username(username):
        """ return airline according to it's user's username. """

        try:
            airline = AirlineCompany.get_airline_by_username(username)
            return airline
        except AirlineCompany.DoesNotExist:
            raise ObjectDoesNotExist(
                f'There is no airline with username: {username}.')

    @staticmethod
    def get_airline_by_name(name):
        try:
            airline = AirlineCompany.get_airline_by_name(name)
            return airline
        except AirlineCompany.DoesNotExist:
            raise ObjectDoesNotExist(
                f'Airline with name {name} does not exists.')

    # ------------------------------------------------------------------------------------------------------------------------------------

    #                                        _____@@@@@@@@@______ ADDITIONAL DAL _____@@@@@@@@@_____

    @staticmethod
    def get_user_by_customer_id(customer_id):
        try:
            customer = DAL.get_by_id(Customer, customer_id)
            customer_user = DAL.get_by_id(User, customer.user.id)
            return customer_user
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist

    @staticmethod
    def get_user_by_airline_id(airline_id):
        try:
            airline = DAL.get_by_id(AirlineCompany, airline_id)
            airline_user = DAL.get_by_id(User, airline.user.id)
            return airline_user
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist

    @staticmethod
    def get_customer_by_phone(phone_no):
        """ use for validation when creating/updating user """
        try:
            customer = Customer.objects.filter(phone_no=phone_no).first()
            if not customer:
                raise ObjectDoesNotExist(
                    f'No customer found with phone number: {phone_no}.')
            return customer
        except Customer.DoesNotExist:
            raise ObjectDoesNotExist(
                f'No customer found with phone number: {phone_no}.')

    @staticmethod
    def get_customer_by_credit(credit):
        """ use for validation when creating/updating user """

        try:
            customer = Customer.objects.filter(credit_card_no=credit).first()
            if not customer:
                raise ObjectDoesNotExist(
                    f'No customer found with credit number: {credit}.')
            return customer
        except Customer.DoesNotExist:
            raise ObjectDoesNotExist(
                f'No customer found with credit number: {credit}.')

    @staticmethod
    def get_airlines_by_country_id(id):
        """ use for validation when creating airline company """
        country = DAL.get_by_id(Country, id)
        try:
            airlines = AirlineCompany.objects.filter(country__id=id)
            if not airlines.exists():
                raise ObjectDoesNotExist(
                    f'There are no airlines in {country.name}.')
            return airlines
        except Country.DoesNotExist:
            raise ObjectDoesNotExist(f'No country found with id {id}.')
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                f'There are no airlines in {country.name}.')

    @staticmethod
    def get_flights_by_origin_country_id(id):
        origin_country = DAL.get_by_id('Country', id)
        try:
            flights = Flight.objects.filter(origin_country__id=id)
            if not flights.exists():
                raise ObjectDoesNotExist(
                    f'There are no flights from {origin_country.name}.')
            return flights
        except Country.DoesNotExist:
            raise ObjectDoesNotExist(f'No country found with id {id}.')
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                f'There are no flights from {origin_country.name}.')

    @staticmethod
    def get_flights_by_destination_country_id(id):
        destination_country = DAL.get_by_id('Country', id)
        try:
            flights = Flight.objects.filter(destination_country__id=id)
            if not flights.exists():
                raise ObjectDoesNotExist(
                    f'There are no flights to {destination_country.name}.')
            return flights
        except Country.DoesNotExist:
            raise ObjectDoesNotExist(f'No country found with id {id}.')
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                f'There are no flights to {destination_country.name}.')

    @staticmethod
    def get_flights_by_departure_date(date):
        try:
            flights = Flight.objects.filter(departure_time=date)
            if not flights.exists():
                raise ObjectDoesNotExist(f'There are no flights on {date}.')
            return flights
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f'There are no flights on {date}.')

    @staticmethod
    def get_flights_by_landing_date(date):
        try:
            flights = Flight.objects.filter(landing_time=date)
            if not flights.exists():
                raise ObjectDoesNotExist(
                    f'There are no flights landing on {date}.')
            return flights
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                f'There are no flights landing on {date}.')

    @staticmethod
    def get_flights_by_customer(customer):
        """ return list of flights that customer bought ticket for. """

        try:
            tickets = Ticket.objects.filter(customer=customer)
            if not tickets.exists():
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
        try:
            tickets = Ticket.objects.filter(flight=flight_id)
            if tickets.exists():
                raise ObjectDoesNotExist(
                    'This flight have sold Tickets: first refund all customers and then try again.')
            return tickets
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                'This flight have sold Tickets: first refund all customers and then try again.')

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

                return {
                    "name": airline_role_data.name,
                    "country":  airline_role_data.country.name,
                    "airline_id": airline_role_data.id
                }
