from .facade_base import FacadeBase
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
            if airline:
                raise Exception
            DAL.create(AirlineCompany, kwargs)
        except KeyError:
            raise KeyError('there is no name')
        except Exception:
            raise Exception(f'There is already airline with name: {name}')


    def add_customer():
        pass


    def add_administrator():
        pass


    def remove_airline(airline):
        pass


    def remove_customer(customer):
        pass


    def remove_administrator(administrator):
        pass