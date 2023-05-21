from django.core.exceptions import ObjectDoesNotExist, ValidationError
from base.models import Country, AirlineCompany, Flight, Customer, Ticket, Administrator, User



class DAL:
    """ class DAL for direct communication with the data base.
    the first 6 method are global to all the models and the rest is model specific """
    
    @staticmethod
    def get_by_id(model, id):
        """ get an instance of a model by his id """
        try:
            return model.objects.get(pk=id)
        except model.DoesNotExist:
            raise ObjectDoesNotExist(f'No {model} found with id {id}')


    @staticmethod
    def get_all(model):
        """ get all instances of a model """
        return model.objects.all()
    

    @staticmethod
    def create(model,**kwargs):
        """ add an instance to a model """
        try:
            obj = model.objects.create(**kwargs)
            return obj
        except ValidationError as e:
            raise ValidationError(f'Error creating {model}: {str(e)}')
        

    @staticmethod
    def add_all(model, items):
        """ add multiple instances of a model at once """
        try:
            return model.objects.bulk_create(items)
        except ValidationError as e:
            raise Exception(f'Error bulk creating {model}: {str(e)} ')
        

    @staticmethod
    def update(model, id, **kwargs):
        """ update an instance of a model """
        instance = DAL.get_by_id(model, id)
        for key, value in kwargs.items():
            # handle only the fields that need to be change
            if hasattr(instance, key):
                setattr(instance, key,  value)
        instance.save()
        return instance


    @staticmethod
    def remove(model, id):
        """ remove an instance of a model """
        instance = DAL.get_by_id(model, id)
        instance.delete()
        return instance
    

    @staticmethod
    def get_airlines_by_country_id(id):
        """ get all the airlines of a country if there is any """
        country = DAL.get_by_id('Country', id)
        try:
            airlines = AirlineCompany.objects.filter(country__id=id).all()
            if not airlines:
                raise ObjectDoesNotExist(f'There are no airlines in {country}')
            return airlines
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f'There are no airlines in {country}')


    @staticmethod
    def get_flights_by_origin_country_id(id):
        """ get all the flights that departure from a country """
        origin_country = DAL.get_by_id('Country', id)
        try:
            flights = Flight.objects.filter(origin_country__id=id).all()
            if not flights:
                raise ObjectDoesNotExist(f'There are no flights from {origin_country}')
            return flights
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f'There are no flights from {origin_country}')
        

    @staticmethod
    def get_flight_by_destination_country_id(id):
        """ gel all the flights that landing in a country """
        destination_country = DAL.get_by_id('Country', id)
        try:
            flights = Flight.objects.filter(destination_country__id=id).all()
            if not flights:
                raise ObjectDoesNotExist(f'There are no flights to {destination_country}')
            return flights
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f'There are no flights to {destination_country}')
        
    @staticmethod
    def get_flights_by_departure_date(date):
        """ get all the flights that departure at a searched date """
        try:
            flights = Flight.objects.filter(departure_time=date)
            if not flights:
                raise ObjectDoesNotExist(f'There are no flights in {date}')
            return flights
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f'There are no flights in {date}')
        

    @staticmethod
    def get_flights_by_landing_date(date):
        """ get all the flights that landing at a searched date """
        try:
            flights = Flight.objects.filter(landing_time=date)
            if not flights:
                raise ObjectDoesNotExist(f'There are no flights landing in {date}')
            return flights
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f'There are no flights landing in {date}')