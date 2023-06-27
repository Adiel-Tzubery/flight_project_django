from .facade_base import FacadeBase, FacadsValidator
from django.contrib.auth import authenticate, login
from django.core.exceptions import PermissionDenied, ValidationError
from dal.dal import DAL
from base.models import User, Customer



class AnonymousFacade(FacadeBase, FacadsValidator):

    # def log_in(request, username, password):
    #     try:
    #         user = authenticate(request, username=username, password=password)
    #         if user is not None:
    #             login(request, user)
    #             return user
    #         else:
    #             raise PermissionDenied(f"Username and password don't match.")
    #     except (PermissionDenied, ValidationError) as e:
    #         raise PermissionDenied("Invalid username or password") from e
    #     except Exception as e:
    #         raise Exception(f"Error: {str(e)}")


    def create_new_user(username, email, password, **kwargs):
        try:
            if not AnonymousFacade.is_username_or_email_exists(username, email):
                user = DAL.create(User, username, email, password, **kwargs)
                return user
        except Exception as e:
            raise Exception(f'Error: {str(e)}.')


    def add_customer(first_name, last_name, credit_card_no, phone_no, address, username, email, password, user_role):
        try:
            user = AnonymousFacade.create_new_user(username, email, password)
            if not AnonymousFacade.is_phone_or_credit_exists(phone_no, credit_card_no):
                customer = DAL.create(Customer, first_name=first_name, last_name=last_name,
                                        credit_card_no=credit_card_no, phone_no=phone_no,
                                        address=address, user=user, user_role=user_role)
                return customer
        except Exception as e:
            raise Exception(f'Error: {str(e)}.')