from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

@staticmethod
def get_flights_by_parameters(origin_country_id=None, destination_country_id=None, date=None):
    """ method that get's all the flights according to parameters if there is any,
        if there isn't the method will return all the flights, if there is any. """
    
    #inserting all the existing conditions to a q
    filter_conditions = Q()

    if origin_country_id is not None:
        filter_conditions &= Q(origin_country=origin_country_id)
    if destination_country_id is not None:
        filter_conditions &= Q(destination_country=destination_country_id)
    if date is not None:
        filter_conditions &= Q(departure_time__date=date)

    # if there are no conditions
    if not filter_conditions:
        try:
            flights = Flight.objects.all()
            if not flights.exists():
                raise ObjectDoesNotExist
            return flights
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist('There are no flights')
        
    # applying the conditions
    try:
        flights = Flight.objects.filter(filter_conditions)
        if not flights.exists():
            raise ObjectDoesNotExist
        return flights
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist('There are no flights matching the parameters')
