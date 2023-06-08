from .facade_base import FacadeBase, FacadsValidator
from .anonymous_facade import AnonymousFacade
from base.models import Customer, AirlineCompany, User
from dal.dal import DAL


class AdministratorFacade(FacadeBase, FacadsValidator):


    def get_all_customers():
        DAL.get_all(Customer)
        

    def add_airline(**kwargs):
        try:
            name = kwargs['name']
            # check if airline already exists
            airline = AdministratorFacade.get_airline_by_parameters(name=name)
            if airline.exists():
                raise Exception
            DAL.create(AirlineCompany, kwargs)
        except KeyError:
            raise KeyError('name not provided')
        except Exception:
            raise Exception(f'There is already airline with name: {name}')


# @@@ needs to be review @@@

    # def add_customer(**kwargs):
    #     try:
    #         phone = kwargs['phone_no']
    #         credit = kwargs['credit_card_no']
    #         customer = DAL.get_customer_by_phone(phone)
    #         if customer.exists():
    #             raise Exception
    #         DAL.create(Customer, kwargs)
    #     except KeyError:
    #         raise KeyError('phone/credit not provided')
    #     except Exception:
    #         raise Exception('customer already exist')


    def add_administrator(**kwargs):
        try: # check if username and email are available.
            username = kwargs['username']
            email = kwargs['email']
            if AdministratorFacade.is_username_or_email_exists(username, email):
                administrator = DAL.create(User, kwargs)
                return administrator
            raise Exception
        except Exception:
            raise Exception


    def remove_airline(airline):
        try: # check if airline exists.
            if AdministratorFacade.is_airline_clear_for_delete(airline):
                DAL.remove(AirlineCompany, airline.id)
        except Exception:
            raise Exception


    def remove_customer(customer):
        try: # check if customer exists.
            if AdministratorFacade.is_customer_clear_for_delete(customer):
                DAL.remove(Customer, customer.id)
        except Exception:
            raise Exception



    def remove_administrator(administrator):
        pass