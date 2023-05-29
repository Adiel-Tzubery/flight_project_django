from django.test import TestCase
from dal.dal import DAL
from base.models import Country, AirlineCompany, Flight, Customer, Ticket, Administrator, User, UserRole
from datetime import datetime, timedelta
from django.utils import timezone





class DalGetAllTests(TestCase):


    @classmethod
    def setUpTestData(cls):
        """ set up class data with instances of classes for the tests methods """

        #create user, administrator objects
        cls.user_role = UserRole.objects.create(role_name='administrator')
        cls.admin_user = User.objects.create(username='ad', password='password', email='ad@gmail.com', user_role=cls.user_role)
        cls.administrator = Administrator.objects.create(first_name='admin', last_name='instrator', user_id=cls.admin_user)


        # create user, country and airline objects
        cls.airline_role = UserRole.objects.create(role_name="airline company")
        cls.airline_user = User.objects.create(username='Beng', password='password', email='bg@gmail.com', user_role=cls.airline_role)
        cls.country = Country.objects.create(name='Israel')
        cls.airline_company = AirlineCompany.objects.create(name='Ben Guryon Airline', country_id=cls.country, user_id=cls.airline_user)

        # create user, administrator and customer objects
        cls.customer_role = UserRole.objects.create(role_name='customer')
        cls.user = User.objects.create(username='avigel', password='password', email='avigel@gmail.com', user_role=cls.customer_role)
        cls.customer = Customer.objects.create(first_name='Avigel', last_name='Tzubery', address='Kfar Hanoar, kfar Hsidim bet', phone_no='5555555555', credit_card_no='2354624632', user_id=cls.user)
        

        # Create flights objects 
        origin_country = DalGetAllTests.country
        destination_country = Country.objects.create(name='Yeman')
        departure_time = datetime(2023,4,16,10,30, tzinfo=timezone.utc)
        landing_time = departure_time + timedelta(hours=6)
        remaining_tickets = 100
        cls.first_flight = Flight.objects.create(
            airline_company_id = DalGetAllTests.airline_company,
            origin_country_id = origin_country,
            destination_country_id = destination_country,
            departure_time = departure_time,
            landing_time = landing_time,
            remaining_tickets = remaining_tickets,
            price = 99
        )
        cls.second_flight = Flight.objects.create(
            airline_company_id = DalGetAllTests.airline_company,
            origin_country_id = origin_country,
            destination_country_id = Country.objects.create(name='Spain'),
            departure_time = departure_time,
            landing_time = landing_time,
            remaining_tickets = remaining_tickets,
            price = 99
        )

        cls.first_ticket = Ticket.objects.create(flight_id=cls.first_flight, customer_id=cls.customer)
        cls.second_ticket = Ticket.objects.create(flight_id=cls.second_flight, customer_id=cls.customer)


    
    # tests for get_all that tests the method action in a all the valid situations

    def test_get_all_successes_country_model(self):
        """ test that the method return the expected country list instance for a valid data """
        excepted_countries = Country.objects.all()
        countries = DAL.get_all(Country)
        self.assertCountEqual(excepted_countries, countries)


    def test_get_all_successes_airline_model(self):
        """ test that the method return the expected airline list instance for a valid data """
        excepted_airlines = AirlineCompany.objects.all()
        airlines = DAL.get_all(AirlineCompany)
        self.assertCountEqual(excepted_airlines, airlines)\
        
        
    def test_get_all_successes_flight_model(self):
        """ test that the method return the expected flight list instance for a valid data """
        excepted_flights = Flight.objects.all()
        flights = DAL.get_all(Flight)
        self.assertCountEqual(excepted_flights, flights)


    def test_get_all_successes_customer_model(self):
        """ test that the method return the expected customer list instance for a valid data """
        excepted_customers = Customer.objects.all()
        customers = DAL.get_all(Customer)
        self.assertCountEqual(excepted_customers, customers)


    def test_get_all_successes_ticket_model(self):
        """ test that the method return the expected ticket list instance for a valid data """
        excepted_tickets = Ticket.objects.all()
        tickets = DAL.get_all(Ticket)
        self.assertCountEqual(excepted_tickets, tickets)


    def test_get_all_successes_administrator_model(self):
        """ test that the method return the expected administrator list instance for a valid data """
        excepted_administrators = Administrator.objects.all()
        administrators = DAL.get_all(Administrator)
        self.assertCountEqual(excepted_administrators, administrators)


    def test_get_all_successes_user_model(self):
        """ test that the method return the expected user list instance for a valid data """
        excepted_users = User.objects.all()
        users = DAL.get_all(User)
        self.assertCountEqual(excepted_users, users)