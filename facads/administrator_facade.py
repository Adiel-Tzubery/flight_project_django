from dal.dal import DAL
from .facade_base import FacadeBase
from .facads_validator import FacadsValidator
from .anonymous_facade import AnonymousFacade
from django.core.exceptions import ObjectDoesNotExist
from base.models import Customer, AirlineCompany, Administrator, Country, User


class AdministratorFacade(FacadeBase):

    def get_all_customers():
        try:
            customers = DAL.get_all(Customer)
            return customers
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist('No customer found.')

    def add_airline(**kwargs):
        try:
            if FacadsValidator.validate_airline_before_creation(kwargs['name'], kwargs['country']):
                    user = AnonymousFacade.create_new_user(
                        username=kwargs['username'],
                        email=kwargs['email'],
                        password=kwargs['password'],
                        user_role=kwargs['user_role']
                    )

            # assign user object to kwargs
            kwargs['user'] = user

            # turning kwargs['country'] from the ID to the instance itself.
            country = DAL.get_by_id(Country, kwargs['country'])
            kwargs['country'] = country
            new_airline = DAL.create(
                AirlineCompany,
                user=kwargs['user'],
                name=kwargs['name'],
                country=kwargs['country'],
            )
            return new_airline
        except KeyError:
            raise KeyError('name not provided')
        except Exception as e:
            raise Exception(f'{str(e)}')

    def add_customer(**kwargs):
        try:
            customer = AnonymousFacade.add_customer(**kwargs)
            return customer
        except Exception as e:
            raise Exception(f'Error: {str(e)}.')

    def add_administrator(**kwargs):
        try:
            user = AnonymousFacade.create_new_user(
                username=kwargs['username'],
                email=kwargs['email'],
                password=kwargs['password'],
                user_role=kwargs['user_role'],
            )
            # assign user object to kwargs
            kwargs['user'] = user
            administrator = DAL.create(
                Administrator,
                first_name=kwargs['first_name'],
                last_name=kwargs['last_name'],
                user=kwargs['user']
            )
            return administrator
        except Exception as e:
            raise Exception(f'Error: {str(e)}.')

    def remove_airline(airline_id):
        try:
            if FacadsValidator.is_airline_clear_for_delete(airline_id):
                airline_user = DAL.get_user_by_airline_id(airline_id)
                deleted_airline = DAL.remove(User, airline_user.id)
                return deleted_airline
            else:
                raise Exception(
                    'Airline have an active flight/s, cannot be removed')
        except Exception as e:
            raise Exception(f'Error: {str(e)}.')

    def remove_customer(customer_id):
        try:
            if FacadsValidator.is_customer_clear_for_delete(customer_id):
                customer_user = DAL.get_user_by_customer_id(customer_id)
                deleted_customer = DAL.remove(User, customer_user.id)
                return deleted_customer
            else:
                raise Exception('Customer have ticket/s, cannot be deleted')
        except Exception as e:
            raise Exception(f'Error: {str(e)}.')

    def remove_administrator(administrator_id):
        try:
            deleted_admin = DAL.remove(Administrator, administrator_id)
            return deleted_admin
        except Exception as e:
            raise Exception(f'Error: {str(e)}.')
