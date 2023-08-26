from .facads_validator import FacadsValidator
from .facade_base import FacadeBase
from dal.dal import DAL
from base.models import User, Customer


class AnonymousFacade(FacadeBase, FacadsValidator):

    def create_new_user(**kwargs):
        try:
            if AnonymousFacade.is_username_not_exists(kwargs['username']):
                if AnonymousFacade.is_email_not_exists(kwargs['email']):
                    user = DAL.create(
                        User,
                        username=kwargs['username'],
                        email=kwargs['email'],
                        password=kwargs['password'],
                        user_role=kwargs['user_role']
                    )
                    return user
        except Exception as e:
            raise Exception(f'Error: {str(e)}.')

    def add_customer(**kwargs):
        try:
            if AnonymousFacade.is_phone_not_exists(kwargs['phone_no']):
                if AnonymousFacade.is_credit_not_exists(kwargs['credit_card_no']):
                    user = AnonymousFacade.create_new_user(
                        username=kwargs['username'],
                        email=kwargs['email'],
                        password=kwargs['password'],
                        user_role=kwargs['user_role']
                    )

                    kwargs['user'] = user
                    customer = DAL.create(
                        Customer,
                        first_name=kwargs['first_name'],
                        last_name=kwargs['last_name'],
                        credit_card_no=kwargs['credit_card_no'],
                        phone_no=kwargs['phone_no'],
                        address=kwargs['address'],
                        user=kwargs['user']
                    )
                    return customer
        except Exception as e:
            raise Exception(f'Error: {str(e)}.')
