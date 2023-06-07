from .facade_base import FacadeBase
from .anonymous_facade import AnonymousFacade
from base.models import Customer, AirlineCompany
from dal.dal import DAL


class AdministratorFacade(FacadeBase):


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


    def add_administrator():
        pass


    def remove_airline(airline):
        pass


    def remove_customer(customer):
        pass


    def remove_administrator(administrator):
        pass