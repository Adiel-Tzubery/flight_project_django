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
    
