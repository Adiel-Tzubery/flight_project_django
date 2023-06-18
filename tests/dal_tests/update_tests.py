from django.test import TestCase
from unittest.mock import patch
from dal.dal import DAL
from base.models import Country, AirlineCompany, Flight, Customer, Ticket, Administrator, User, UserRole
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
from django.utils import timezone




class DalUpdateTests(TestCase):


    @classmethod
    def setUpTestData(cls):
        """ set up class data with instances of classes for the tests methods """

        #create user, administrator objects
        cls.admin_role = UserRole.objects.create(role_name='administrator')
        cls.admin_user = User.objects.create(username='ad', password='password', email='ad@gmail.com', user_role=cls.admin_role)
        cls.administrator = Administrator.objects.create(first_name='admin', last_name='instrator', user=cls.admin_user)


        # create user, country and airline objects
        cls.airline_role = UserRole.objects.create(role_name='airline company')
        cls.airline_user = User.objects.create(username='Beng', password='password', email='bg@gmail.com', user_role=cls.airline_role)
        cls.country = Country.objects.create(name='Israel')
        cls.airline_company = AirlineCompany.objects.create(name='Ben Guryon Airline', country=cls.country, user=cls.airline_user)

        # create user, administrator and customer objects
        cls.customer_role = UserRole.objects.create(role_name='customer')
        cls.user = User.objects.create(username='avigel', password='password', email='avigel@gmail.com', user_role=cls.customer_role)
        cls.customer = Customer.objects.create(first_name='Avigel', last_name='Tzubery', address='Kfar Hanoar, kfar Hsidim bet', phone_no='555-555-5555', credit_card_no='2354624632', user=cls.user)
        

        # Create flights objects 
        origin_country = DalUpdateTests.country
        destination_country = Country.objects.create(name='Yeman')
        departure_time = datetime(2023,4,16,10,30, tzinfo=timezone.utc)
        landing_time = departure_time + timedelta(hours=6)
        remaining_tickets = 100
        cls.first_flight = Flight.objects.create(
            airline_company = DalUpdateTests.airline_company,
            origin_country = origin_country,
            destination_country = destination_country,
            departure_time = departure_time,
            landing_time = landing_time,
            remaining_tickets = remaining_tickets,
            price = 99
        )
        cls.second_flight = Flight.objects.create(
            airline_company = DalUpdateTests.airline_company,
            origin_country = origin_country,
            destination_country = Country.objects.create(name='Spain'),
            departure_time = departure_time,
            landing_time = landing_time,
            remaining_tickets = remaining_tickets,
            price = 99
        )

        cls.first_ticket = Ticket.objects.create(flight=cls.first_flight, customer=cls.customer)
        cls.second_ticket = Ticket.objects.create(flight=cls.second_flight, customer=cls.customer)


    def test_update_successes_country(self):
        """ test that the method changing successfully the country object """
        country = DalUpdateTests.country
        country_id = country.id
        new_name = 'Uzbekistan'
        updated_country = DAL.update(Country, country_id, name=new_name)
        new_country = DAL.get_by_id(Country, country_id)
        self.assertEqual(updated_country, new_country)