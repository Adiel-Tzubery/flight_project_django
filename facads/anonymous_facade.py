from .facade_base import FacadeBase



class AnonymousFacade(FacadeBase):


    def log_in(username, password):
        pass


    def create_new_user(username, email, password, **kwargs):
        DAL.create(User, username, email, password, **kwargs)


    def add_customer():
        pass