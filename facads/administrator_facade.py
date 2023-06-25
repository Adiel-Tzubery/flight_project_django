from dal.dal import DAL
from .facade_base import FacadeBase, FacadsValidator
from .anonymous_facade import AnonymousFacade
from django.core.exceptions import ObjectDoesNotExist
from base.models import Customer, AirlineCompany, User, Administrator


class AdministratorFacade(FacadeBase):

    def get_all_customers():
        try:
            customers = DAL.get_all(Customer)
            return customers
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist('No customer found.')

    def add_airline(**kwargs):
        try:
            name = kwargs['name']
            # check if airline already exists
            airline = AdministratorFacade.get_airline_by_parameters(name=name)
            if airline.exists():
                raise Exception(f'There is already airline with name: {name}.')
            new_airline = DAL.create(AirlineCompany, kwargs)
            return new_airline
        except KeyError:
            raise KeyError('name not provided')
        except Exception:
            raise Exception(f'There is already airline with name: {name}.')

    def add_customer(**kwargs):
        try:
            customer = AnonymousFacade.add_customer(kwargs)
            return customer
        except Exception as e:
            raise Exception(f'Error: {str(e)}.')

    def add_administrator(**kwargs):
        try:  # check if username and email are available.
            username = kwargs['username']
            email = kwargs['email']
            if not FacadsValidator.is_username_or_email_exists(username, email):
                administrator = DAL.create(User, kwargs)
                return administrator
        except Exception as e:
            raise Exception(f'Error: {str(e)}.')

    def remove_airline(airline_id):
        try:  # check if airline exists.
            if FacadsValidator.is_airline_clear_for_delete(airline_id):
                deleted_airline = DAL.remove(AirlineCompany, airline_id)
                return deleted_airline
        except Exception:
            raise Exception

    def remove_customer(customer_id):
        try:  # check if customer exists.
            if FacadsValidator.is_customer_clear_for_delete(customer_id):
                deleted_customer = DAL.remove(Customer, customer_id)
                return deleted_customer
        except Exception as e:
            raise Exception(f'Error: {str(e)}.')

    def remove_administrator(administrator_id):
        try:
            deleted_admin = DAL.remove(Administrator, administrator_id)
            return deleted_admin
        except Exception as e:
            raise Exception(f'Error: {str(e)}.')
