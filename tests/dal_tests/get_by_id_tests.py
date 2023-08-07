from django.test import TestCase
from unittest.mock import patch
from dal.dal import DAL
from base.models import Country, AirlineCompany, Flight, Customer, Ticket, Administrator, User, UserRole
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
from django.utils import timezone


# create a temporary model for testing
# class TempModel(models.Model):
#     app_label = 'base'


class DalGetByIdTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """ set up class data with instances of classes for the tests methods """

        # create user, administrator objects
        cls.admin_role = UserRole.objects.create(role_name='administrator')
        cls.admin_user = User.objects.create(
            username='ad', password='password', email='ad@gmail.com', user_role=cls.admin_role)
        cls.administrator = Administrator.objects.create(
            first_name='admin', last_name='instrator', user=cls.admin_user)

        # create user, country and airline objects
        cls.airline_role = UserRole.objects.create(role_name='airline company')
        cls.airline_user = User.objects.create(
            username='Beng', password='password', email='bg@gmail.com', user_role=cls.airline_role)
        cls.country = Country.objects.create(name='Israel')
        cls.airline_company = AirlineCompany.objects.create(
            name='Ben Guryon Airline', country=cls.country, user=cls.airline_user)

        # create user, administrator and customer objects
        cls.customer_role = UserRole.objects.create(role_name='customer')
        cls.user = User.objects.create(
            username='avigel', password='password', email='avigel@gmail.com', user_role=cls.customer_role)
        cls.customer = Customer.objects.create(first_name='Avigel', last_name='Tzubery', address='Kfar Hanoar, kfar Hsidim bet',
                                               phone_no='555-555-5555', credit_card_no='2354624632', user=cls.user)

        # Create flights objects
        origin_country = DalGetByIdTests.country
        destination_country = Country.objects.create(name='Yeman')
        departure_time = datetime(2023, 4, 16, 10, 30, tzinfo=timezone.utc)
        landing_time = departure_time + timedelta(hours=6)
        remaining_tickets = 100
        cls.first_flight = Flight.objects.create(
            airline_company=DalGetByIdTests.airline_company,
            origin_country=origin_country,
            destination_country=destination_country,
            departure_time=departure_time,
            landing_time=landing_time,
            remaining_tickets=remaining_tickets,
            price=99
        )
        cls.second_flight = Flight.objects.create(
            airline_company=DalGetByIdTests.airline_company,
            origin_country=origin_country,
            destination_country=Country.objects.create(name='Spain'),
            departure_time=departure_time,
            landing_time=landing_time,
            remaining_tickets=remaining_tickets,
            price=99
        )

        cls.first_ticket = Ticket.objects.create(
            flight=cls.first_flight, customer=cls.customer)
        cls.second_ticket = Ticket.objects.create(
            flight=cls.second_flight, customer=cls.customer)

    # 7 tests for get_by_id that tests the method action in a all the valid situations

    def test_get_by_id_successes_with_existing_country(self):
        """ test that the method return the expected country instance for a valid data """
        country_id = DalGetByIdTests.country.id
        expected_country = DAL.get_by_id(Country, country_id)
        self.assertEqual(expected_country, DalGetByIdTests.country)

    def test_get_by_id_successes_with_existing_airline(self):
        """ test that the method return the expected airline instance for a valid data """
        airline_id = DalGetByIdTests.airline_company.id
        expected_airline = DAL.get_by_id(AirlineCompany, airline_id)
        self.assertEqual(expected_airline, DalGetByIdTests.airline_company)

    def test_get_by_id_successes_with_existing_flight(self):
        """ test that the method return the expected flight instance for a valid data """
        flight_id = DalGetByIdTests.first_flight.id
        expected_flight = DAL.get_by_id(Flight, flight_id)
        self.assertEqual(expected_flight, DalGetByIdTests.first_flight)

    def test_get_by_id_successes_with_existing_customer(self):
        """ test that the method return the expected customer instance for a valid data """
        customer_id = DalGetByIdTests.customer.id
        expected_customer = DAL.get_by_id(Customer, customer_id)
        self.assertEqual(expected_customer, DalGetByIdTests.customer)

    def test_get_by_id_successes_with_existing_ticket(self):
        """ test that the method return the expected ticket instance for a valid data """
        ticket_id = DalGetByIdTests.first_ticket.id
        expected_ticket = DAL.get_by_id(Ticket, ticket_id)
        self.assertEqual(expected_ticket, DalGetByIdTests.first_ticket)

    def test_get_by_id_successes_with_existing_administrator(self):
        """ test that the method return the expected administrator instance for a valid data """
        administrator_id = DalGetByIdTests.administrator.id
        expected_administrator = DAL.get_by_id(Administrator, administrator_id)
        self.assertEqual(expected_administrator, DalGetByIdTests.administrator)

    def test_get_by_id_successes_with_existing_user(self):
        """ test that the method return the expected user instance for a valid data """
        user_id = DalGetByIdTests.user.id
        expected_user = DAL.get_by_id(User, user_id)
        self.assertEqual(expected_user, DalGetByIdTests.user)

    # tests for get_by_id with invalid situations, the method expected ro raise an error

    # def test_get_by_id_failure_with_non_existing_model(self):
    #     non_existing_model = DalGetByIdTests.TempModel
    #     some_id = 99
    #     with self.assertRaises(ObjectDoesNotExist):
    #         DAL.get_by_id(non_existing_model, some_id)

    # 7 tests for get_by_id that tests the method action in a all the invalid situations

    def test_get_by_id_failure_with_non_existing_country(self):
        """ test that the method raise the expected error instance for a non valid data """
        country_id = 99
        with self.assertRaises(ObjectDoesNotExist):
            DAL.get_by_id(Country, country_id)

    def test_get_by_id_failure_with_non_existing_airline(self):
        """ test that the method raise the expected error instance for a non valid data """
        airline_id = 99
        with self.assertRaises(ObjectDoesNotExist):
            DAL.get_by_id(AirlineCompany, airline_id)

    def test_get_by_id_failure_with_non_existing_flight(self):
        """ test that the method raise the expected error instance for a non valid data """
        flight_id = 99
        with self.assertRaises(ObjectDoesNotExist):
            DAL.get_by_id(Flight, flight_id)

    def test_get_by_id_failure_with_non_existing_customer(self):
        """ test that the method raise the expected error instance for a non valid data """
        customer_id = 99
        with self.assertRaises(ObjectDoesNotExist):
            DAL.get_by_id(Customer, customer_id)

    def test_get_by_id_failure_with_non_existing_ticket(self):
        """ test that the method raise the expected error instance for a non valid data """
        ticket_id = 99
        with self.assertRaises(ObjectDoesNotExist):
            DAL.get_by_id(Ticket, ticket_id)

    def test_get_by_id_failure_with_non_existing_administrator(self):
        """ test that the method raise the expected error instance for a non valid data """
        administrator_id = 99
        with self.assertRaises(ObjectDoesNotExist):
            DAL.get_by_id(Administrator, administrator_id)

    def test_get_by_id_failure_with_non_existing_user(self):
        """ test that the method raise the expected error instance for a non valid data """
        user_id = 99
        with self.assertRaises(ObjectDoesNotExist):
            DAL.get_by_id(User, user_id)
