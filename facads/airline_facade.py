from .facade_base import FacadeBase, FacadsValidator
from django.core.exceptions import ObjectDoesNotExist
from dal.dal import DAL
from base.models import AirlineCompany, Flight


class AirlineFacade(FacadeBase):


    def update_airline(airline_id, **kwargs):
        try:
            flight = DAL.update(AirlineCompany, airline_id, kwargs)
            return flight
        except Exception:
            raise Exception


    def add_flight(**kwargs):
        try:
            if FacadsValidator.is_flight_valid(kwargs):
                flight = DAL.create(Flight, kwargs)
                return flight
        except Exception:
            raise Exception


    def update_flight(flight_id, **kwargs):
        try:
            origin_country=kwargs['origin_country']
            destination_country=kwargs['destination_country']
            departure_time=kwargs['departure_time']
            landing_time=kwargs['landing_time']
            remaining_tickets=kwargs['remaining_tickets']
            price=kwargs['price']
            if FacadsValidator.is_flight_valid(origin_country=origin_country,
                                            destination_country=destination_country,
                                            departure_time=departure_time,
                                            landing_time=landing_time,
                                            remaining_tickets=remaining_tickets,
                                            price=price):
                updated_flight = DAL.update(Flight, flight_id, origin_country=origin_country,
                                            destination_country=destination_country,
                                            departure_time=departure_time,
                                            landing_time=landing_time,
                                            remaining_tickets=remaining_tickets,
                                            price=price)
                return updated_flight
        except Exception:
            raise Exception
            



    def remove_flight(flight_id):
        try: # check if flight soled any tickets.
            if DAL.get_tickets_by_flight_id(flight_id):
                raise Exception('This flight have sold Tickets: cannot be deleted')
            deleted_flight = DAL.remove(Flight, flight_id)
            return deleted_flight
            # return something
        except Exception:
            raise Exception('This flight have sold Tickets: cannot be deleted')
 


    def get_my_flights(airline_id):
        try:
            flights = DAL.get_flights_by_airline_id(airline_id=airline_id)
            return flights
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist('This airline has no flights')
