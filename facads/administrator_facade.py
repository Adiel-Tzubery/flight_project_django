from dal.dal import DAL
from .facade_base import FacadeBase, FacadsValidator
from .anonymous_facade import AnonymousFacade
from django.core.exceptions import ObjectDoesNotExist
from base.models import Customer, AirlineCompany, Administrator, Country


class AdministratorFacade(FacadeBase):

    def get_all_customers():
        """ return list of all the customers, if there are any. """

        try:
            customers = DAL.get_all(Customer)
            return customers
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist('No customer found.')

    def add_airline(**kwargs):
        """ create and return new airline if data passes validations. """

        try:
            # check if airline already exists. (name is unique)
            if FacadsValidator.is_airline_name_not_exists(kwargs['name']):
                if FacadsValidator.is_country_has_no_airline(kwargs['country']):
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
            raise Exception(f'error: {str(e)}')

    def add_customer(**kwargs):
        """ create and return new customer if data passes validations. """

        try:
            customer = AnonymousFacade.add_customer(**kwargs)
            return customer
        except Exception as e:
            raise Exception(f'Error: {str(e)}.')

    def add_administrator(**kwargs):
        """ create and return new administrator if data passes validations. """

        try:  # check if username and email are available.
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
        """ remove airline. """

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
            else:
                raise Exception('Customer have ticket/s, cannot be deleted')
        except Exception as e:
            raise Exception(f'Error: {str(e)}.')

    def remove_administrator(administrator_id):
        """ delete and return administrator. """

        try:
            deleted_admin = DAL.remove(Administrator, administrator_id)
            return deleted_admin
        except Exception as e:
            raise Exception(f'Error: {str(e)}.')
