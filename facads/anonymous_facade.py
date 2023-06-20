from .facade_base import FacadeBase, FacadsValidator
from dal.dal import DAL
from base.models import User, Customer



class AnonymousFacade(FacadeBase, FacadsValidator):

    def log_in(username, password):
        pass


    def create_new_user(username, email, password, **kwargs):
        try:
            if not AnonymousFacade.is_username_or_email_exists(username, email):
                user = DAL.create(User, username, email, password, **kwargs)
                return user
        except Exception as e:
            raise Exception(f'Error: {str(e)}.')


    def add_customer(first_name, last_name, credit_card_no, phone_no, address, username, email, password):
        try:
            user = AnonymousFacade.create_new_user(username, email, password)
            if not AnonymousFacade.is_phone_or_credit_exists(phone_no, credit_card_no):
                customer = DAL.create(Customer, first_name=first_name, last_name=last_name,
                                        credit_card_no=credit_card_no, phone_no=phone_no,
                                        address=address, user=user)
                return customer
        except Exception as e:
            raise Exception(f'Error: {str(e)}.')