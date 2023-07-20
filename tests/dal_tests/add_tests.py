from django.test import TestCase
from dal.dal import DAL
from base.models import Country, AirlineCompany, Flight, UserRole, Customer, Ticket, Administrator, User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from datetime import datetime, timedelta
from django.utils import timezone


class DalAddTests(TestCase):

    


    def setUp(self):
        
        # roles
        self.customer_role = UserRole.objects.create(role_name='customer')
        self.administrator_role = UserRole.objects.create(role_name='administrator')
        self.airline_role = UserRole.objects.create(role_name='airline company')
        
        # countries
        self.airline_country = Country.objects.create(name='spain')
        self.destination_country = Country.objects.create(name='yemen')

        # airline
        self.user = User.objects.create(username='Ben-Guryon', email='bg@gmail.com', password='password')
        self.country = Country.objects.create(name='Israel')
        self.airline_company = DAL.create(AirlineCompany, name='Ben Guryon Airline', country=self.country, user=self.user, user_role=self.airline_role)

        # customer
        self.user = User.objects.create_user(username='adieltzu', email='shalom@gmail.com', password='password')
        self.customer = DAL.create(Customer,first_name='Adiel',
                                                last_name='Tzubery',
                                                phone_no='056-9856925',
                                                credit_card_no='0452-0527-9856-9874',
                                                user=self.user,
                                                user_role=self.customer_role)
        
        # flight
        airline_company = self.airline_company
        origin_country = self.country
        destination_country = self.destination_country
        departure_time = datetime(2023,4,16,10,30, tzinfo=timezone.utc)
        landing_time = departure_time + timedelta(hours=6)
        remaining_tickets = 100
        price = 99
        self.flight = Flight.objects.create(airline_company=airline_company,
                                        origin_country=origin_country,
                                        destination_country=destination_country,
                                        departure_time=departure_time,
                                        landing_time=landing_time,
                                        remaining_tickets=remaining_tickets,
                                        price=price)



    def test_create_country(self):
        name = 'Fiji'
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
        user_role = 'customer'
        user = DAL.create(User, username=username, email=email, password=password)
        first_name = 'Nave'
        last_name = 'Alon'
        credit_card_no = '5555-5555-5555-5555'
        phone_no = '054-5423-2343'
        address = 'kfar hasidim'
        customer = DAL.create(Customer,first_name=first_name, last_name=last_name, credit_card_no=credit_card_no, phone_no=phone_no, address=address, user_role=user_role, user=user)
        expected_customer = DAL.get_customer_by_username(username)
        self.assertEqual(expected_customer, customer)


    def test_create_administrator(self):
        username = 'admin'
        email = 'admin@mail.com'
        password = 'password'
        user_role = 'administrator'
        user = DAL.create(User,username=username, email=email, password=password,)
        first_name = 'add'
        last_name = 'min'
        administrator = DAL.create(Administrator, first_name=first_name, last_name=last_name, user=user)
        # by email: unique
        expected_admin = DAL.get_user_by_email(email).first()
        self.assertEqual(expected_admin.email, administrator.user.email)


    def test_create_airline(self):
        username = 'airlineuser'
        email = 'air@line.com'
        password = 'password'
        user_role = 'airline company'
        user = DAL.create(User, username=username, email=email, password=password)
        name = 'spainaire'
        airline = DAL.create(AirlineCompany, name=name, country=self.airline_country, user=user, user_role=user_role)
        expected_airline = DAL.get_airline_by_username(username)
        self.assertEqual(expected_airline, airline)


    def test_create_flight(self):
        airline_company = self.airline_company
        origin_country = self.airline_country
        destination_country = self.destination_country
        departure_time = datetime(2022,4,16,10,30, tzinfo=timezone.utc)
        landing_time = departure_time + timedelta(hours=6)
        remaining_tickets = 100
        price = 99
        flight = DAL.create(Flight, airline_company=airline_company,
                            origin_country=origin_country,
                            destination_country=destination_country,
                            departure_time=departure_time,
                            landing_time=landing_time,
                            remaining_tickets=remaining_tickets,
                            price=price)
        expected_flight = DAL.get_flights_by_departure_date(departure_time).first()
        self.assertEqual(expected_flight, flight)


    def test_create_ticket(self):
        customer = self.customer
        flight = self.flight
        ticket = DAL.create(Ticket, customer=customer, flight=flight)
        expected_ticket = DAL.get_tickets_by_customer_id(customer.id).first()
        self.assertEqual(expected_ticket, ticket)
