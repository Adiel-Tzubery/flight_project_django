from .facads_validator import FacadsValidator
from .facade_base import FacadeBase
from django.core.exceptions import ObjectDoesNotExist
from dal.dal import DAL
from base.models import AirlineCompany, Flight, Country, User
from django.contrib.auth.hashers import check_password

from dateutil import parser
from datetime import datetime
import pytz


class AirlineFacade(FacadeBase):

    def update_airline(**kwargs):
        """ return updated airline if the data passes validations. """
        airline = DAL.get_by_id(AirlineCompany, kwargs['airline_id'])

        try:  # data validations
            if airline.user.username != kwargs['username'] and FacadsValidator.is_username_not_exists(username=kwargs['username']) or airline.user.username == kwargs['username']:
                if airline.user.email != kwargs['email'] and FacadsValidator.is_email_not_exists(kwargs['email']) or airline.user.email == kwargs['email']:

                    # if there is new password, set it, else set it to original
                    if kwargs['new_password'] != '':
                        if check_password(kwargs['password'], airline.user.password):
                            kwargs['password'] = kwargs['new_password']
                        else:
                            raise Exception('old password not match')
                    else:
                        kwargs['password'] = airline.user.password

                    # update user
                    id = airline.user.id  # to user id
                    DAL.update(
                        User,
                        id,
                        username=kwargs['username'],
                        email=kwargs['email'],
                    )

                    # update airline
                    id = kwargs['airline_id']  # to airline id
                    updated_airline = DAL.update(
                        AirlineCompany,
                        id,
                        password=kwargs['password'],
                        name=kwargs['name'])
                    return updated_airline
        except Exception as e:
            raise Exception(f'{str(e)}')

    def add_flight(**kwargs):
        """ create and return new flight if data passes validations. """

        # convert to datetime objects
        kwargs['departure_time'] = parser.parse(kwargs['departure_time'])
        kwargs['landing_time'] = parser.parse(kwargs['landing_time'])

        try:
            if FacadsValidator.is_flight_valid(**kwargs):

                # converting from id to the actual objects
                kwargs['airline_company'] = DAL.get_by_id(
                    AirlineCompany, kwargs['airline_company'])
                kwargs['origin_country'] = DAL.get_by_id(
                    Country, kwargs['origin_country'])
                kwargs['destination_country'] = DAL.get_by_id(
                    Country, kwargs['destination_country'])
                flight = DAL.create(Flight, **kwargs)
                return flight
        except Exception as e:
            raise Exception(f'{str(e)}')

    def update_flight(**kwargs):
        """ return updated airline if the data passes validations. """

        try:

            # convert countries to their id's
            origin_country = DAL.get_country_by_name(
                name=kwargs['origin_country'])
            destination_country = DAL.get_country_by_name(
                name=kwargs['destination_country'])

            # convert to datetime object (offset-aware)
            departure_time = parser.parse(
                kwargs['departure_time']).astimezone(pytz.UTC)
            landing_time = parser.parse(
                kwargs['landing_time']).astimezone(pytz.UTC)

            flight_id = kwargs['flight_id']
            airline_company = kwargs['airline_company']
            remaining_tickets = kwargs['remaining_tickets']
            price = kwargs['price']
            if FacadsValidator.is_flight_valid(
                airline_company=airline_company,
                flight_id=flight_id, origin_country=origin_country.id,
                destination_country=destination_country.id,
                departure_time=departure_time,
                landing_time=landing_time,
                remaining_tickets=remaining_tickets,
                price=price
            ):

                # update and return the flight.
                updated_flight = DAL.update(Flight, flight_id, origin_country=origin_country,
                                            destination_country=destination_country,
                                            departure_time=departure_time,
                                            landing_time=landing_time,
                                            remaining_tickets=remaining_tickets,
                                            price=price)
                return updated_flight
        except Exception as e:
            raise Exception(f'{str(e)}')

    def remove_flight(flight_id):
        """ only if flight landed/haven't sold any tickets/all tickets returned """
        try:
            flight = DAL.get_by_id(Flight, flight_id)
            # if flight landed, continue. if not, check for ticket/s.
            if flight.landing_time >= datetime.now(pytz.UTC):
                # have flight soled any tickets.
                DAL.get_tickets_by_flight_id(flight_id)
            deleted_flight = DAL.remove(Flight, flight_id)
            return deleted_flight
        except Exception as e:
            raise Exception(f'{str(e)}')

    def get_my_flights(airline_id):
        """ return list of all the flights of airline company, is there is any. """

        try:
            flights = DAL.get_flights_by_airline_id(airline_id=airline_id)
            return flights
        except ObjectDoesNotExist as e:
            raise ObjectDoesNotExist(f'Error: {str(e)}')
