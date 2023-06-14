from .facade_base import FacadeBase, FacadsValidator
from dal.dal import DAL
from base.models import AirlineCompany, Flight


class AirlineFacade(FacadeBase):


    def update_airline(airline, **kwargs):
        try:
            DAL.update(AirlineCompany, airline.id, kwargs)
        except Exception:
            raise Exception


    def add_flight(**kwargs):
        try:
            if FacadsValidator.is_flight_valid(kwargs):
                DAL.create(Flight, kwargs)
        except Exception:
            raise Exception


    def update_flight(flight, **kwargs):
        try: # first check parameters to change
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
                updated_flight = DAL.update(Flight, origin_country=origin_country,
                                               destination_country=destination_country,
                                               departure_time=departure_time,
                                               landing_time=landing_time,
                                               remaining_tickets=remaining_tickets,
                                               price=price)
                return updated_flight
        except Exception:
            raise Exception
            



    def remove_flight(flight):
        pass


    def get_my_flights():
        pass