from django.test import TestCase
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from base.models import Country, AirlineCompany, Flight, Customer, Ticket, User, UserRole


class TicketModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):      
        cls.create_customer()
        cls.create_airline_company()
        cls.create_flights()


    @classmethod
    def create_customer(cls):
        # create customer object for the whole test class
        cls.customer_rol = UserRole.objects.create(role_name='customer')
        cls.user = User.objects.create_user(username='avigel', password='password', email='avigel@gmail.com', user_role=cls.customer_rol)
        cls.customer = Customer.objects.create(first_name='Avigel', last_name='Tzubery', address='Kfar Hanoar, kfar Hsidim bet', phone_no='555-555-5555', credit_card_no='2354624632', user=cls.user)


    @classmethod
    def create_airline_company(cls):
        # Create airline company object for the whole test class
        cls.airline_rol = UserRole.objects.create(role_name='airline company')
        cls.airline_user = User.objects.create_user(username='Beng', password='password', email='bg@gmail.com', user_role=cls.airline_rol)
        cls.country = Country.objects.create(name='Israel')
        cls.airline_company = AirlineCompany.objects.create(name='Ben Guryon Airline', country=cls.country, user=cls.airline_user)

    
    @classmethod
    def create_flights(cls):
        # Create flights object for each test case 
        origin_country = TicketModelTests.country
        destination_country = Country.objects.create(name='Yeman')
        departure_time = datetime(2023,4,16,10,30, tzinfo=timezone.utc)
        landing_time = departure_time + timedelta(hours=6)
        remaining_tickets = 100
        cls.first_flight = Flight.objects.create(
            airline_company = TicketModelTests.airline_company,
            origin_country = origin_country,
            destination_country = destination_country,
            departure_time = departure_time,
            landing_time = landing_time,
            remaining_tickets = remaining_tickets,
            price = 99
        )
        cls.second_flight = Flight.objects.create(
            airline_company = TicketModelTests.airline_company,
            origin_country = origin_country,
            destination_country = Country.objects.create(name='Spain'),
            departure_time = departure_time,
            landing_time = landing_time,
            remaining_tickets = remaining_tickets,
            price = 99
        )


    def setUp(self):
        # set up method that add 2 tickets for the class customer
        self.first_ticket = Ticket.objects.create(flight=TicketModelTests.first_flight, customer=TicketModelTests.customer)
        self.second_ticket = Ticket.objects.create(flight=TicketModelTests.second_flight, customer=TicketModelTests.customer)


    def test_get_tickets_by_customer_without_any_tickets(self):
        # test that the method raises the expected error in the case that the customer has zero tickets
        self.first_ticket.delete()
        self.second_ticket.delete()
        customer_id = TicketModelTests.customer.id
        expected_message = f'No tickets found for customer {customer_id}'
        with self.assertRaises(ObjectDoesNotExist):
            Ticket.get_tickets_by_customer(customer_id)        


    def test_get_tickets_by_customer_success(self):
        # test that the method return successfully all the customer's tickets
        customer_id = TicketModelTests.customer.id
        expected_tickets = [self.first_ticket, self.second_ticket]
        tickets = Ticket.get_tickets_by_customer(customer_id)
        self.assertCountEqual(tickets,expected_tickets)


    def test_get_tickets_by_customer_without_any_tickets_spesific_customer(self):
        # test that the method return only the customer id's much's tickets
        customer_id = TicketModelTests.customer.id
        user = User.objects.create_user(username='adielt', password='password', email='adiel@gmail.com', user_role=TicketModelTests.customer_rol)
        adiel = Customer.objects.create(first_name='adiel', last_name='Tzubery', address='Kfar Hanoar, kfar Hsidim bet', phone_no='666-666-6666', credit_card_no='7654565436', user=user)
        a_tickets = Ticket.objects.create(flight=TicketModelTests.first_flight, customer=adiel)
        adiel_tickets = Ticket.get_tickets_by_customer(adiel.id)
        tickets = Ticket.get_tickets_by_customer(customer_id)
        self.assertEqual(tickets.count(), 2)
        self.assertEqual(tickets[0].customer, self.customer)
        self.assertEqual(adiel_tickets[0].customer, adiel)

    
    def test_get_tickets_by_customer_with_non_existing_customer(self):
        customer_id = '999'
        expected_message = f'No customer found with ID {customer_id}'
        with self.assertRaises(ObjectDoesNotExist, msg=expected_message):
            Ticket.get_tickets_by_customer(customer_id)