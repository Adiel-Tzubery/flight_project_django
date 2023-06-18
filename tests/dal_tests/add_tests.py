from django.test import TestCase
from dal.dal import DAL
from base.models import Country, AirlineCompany, Flight, Customer, Ticket, Administrator, User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from datetime import datetime, timedelta
from django.utils import timezone


class DalAddTests(TestCase):

    def test_create_country(self):
        name = 'Israel'
        country = DAL.create(Country, name=name)
        expected_country = DAL.get_by_id(Country, country.id)
        self.assertEqual(expected_country, country)
    

    def test_create_user(self):
        username = 'username'
        email = 'email@email.com'
        password = 'password'
        user = DAL.create(User, username=username, email=email, password=password)
        expected_user = DAL.get_user_by_username(username)
        self.assertEqual(expected_user, user)


    def test_create_customer(self):
        username = 'username'
        email = 'email@email.com'
        password = 'password'
        user = DAL.create(User, username=username, email=email, password=password)
        customer = DAL.create(Customer, )