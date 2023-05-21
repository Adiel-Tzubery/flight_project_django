from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from base.models import User, AirlineCompany, Country, Flight
from datetime import datetime, timedelta
from django.utils import timezone



class FlightModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create airline company object for the whole test class
        cls.user = User.objects.create(username='Ben-Guryon', password='password', email='bg@gmail.com', user_role='Airline Company')
        cls.country = Country.objects.create(name='Israel')
        cls.airline_company = AirlineCompany.objects.create(name='Ben Guryon Airline', country=cls.country, user=cls.user)


    def setUp(self):
        # Create flights object for each test case 
        origin_country = FlightModelTest.country
        destination_country = Country.objects.create(name='Yeman')
        departure_time = datetime(2023,4,16,10,30, tzinfo=timezone.utc)
        landing_time = departure_time + timedelta(hours=6)
        remaining_tickets = 100
        self.flight = Flight.objects.create(
            airline_company = FlightModelTest.airline_company,
            origin_country = origin_country,
            destination_country = destination_country,
            departure_time = departure_time,
            landing_time = landing_time,
            remaining_tickets = remaining_tickets
        )
        self.another_flight = Flight.objects.create(
            airline_company = FlightModelTest.airline_company,
            origin_country = origin_country,
            destination_country = Country.objects.create(name='Spain'),
            departure_time = departure_time,
            landing_time = landing_time,
            remaining_tickets = remaining_tickets
        )


    def test_get_flights_by_parameters_success_with_all_parameters(self):
        # Test if the method returns the flights as expected when entering the right parameters(all of theme)
        departure_time = datetime(2023,4,16,10,30, tzinfo=timezone.utc)
        origin_country_id = FlightModelTest.country.id
        destination_country_id = self.flight.destination_country.id
        expected_flights = [self.flight]
        flights = Flight.get_flights_by_parameters(origin_country_id, destination_country_id, departure_time)
        self.assertCountEqual(flights, expected_flights)


    def test_get_flights_by_parameters_success_only_with_origin_and_destination_countries(self):
        # Test if the method returns the flights as expected when entering the right parameters(only origin and destination countries)
        origin_country_id = FlightModelTest.country.id
        destination_country_id = self.flight.destination_country.id
        expected_flights = [self.flight]
        flights = Flight.get_flights_by_parameters(origin_country_id,destination_country_id)
        self.assertCountEqual(flights, expected_flights)


    def test_get_flights_by_parameters_success_only_with_origin_country_and_departure_time(self):
        # Test if the method returns the flights as expected when entering the right parameters(only origin country and departure time)
        departure_time = datetime(2023,4,16,10,30, tzinfo=timezone.utc)
        origin_country_id = FlightModelTest.country.id
        expected_flights = [self.flight]
        flights = Flight.get_flights_by_parameters(origin_country_id=origin_country_id, departure_time=departure_time)
        self.assertEqual(flights[0], expected_flights[0])


    def test_get_flights_by_parameters_success_only_with_destination_country_and_departure_time(self):
        # Test if the method returns the flights as expected when entering the right parameters(only destination country and departure time)
        departure_time = datetime(2023,4,16,10,30, tzinfo=timezone.utc)
        destination_country_id = self.flight.destination_country.id
        expected_flights = [self.flight]
        flights = Flight.get_flights_by_parameters(destination_country_id=destination_country_id, departure_time=departure_time)
        self.assertCountEqual(flights, expected_flights)


    def test_get_flights_by_parameters_success_only_with_origin_country(self):
        # Test if the method returns the flights as expected when entering the right parameters(only origin country)
        origin_country_id = FlightModelTest.country.id
        expected_flights = [self.flight]
        flights = Flight.get_flights_by_parameters(origin_country_id=origin_country_id)
        self.assertEqual(flights[0], expected_flights[0])


    def test_get_flights_by_parameters_success_only_with_destination_country(self):
        # Test if the method returns the flights as expected when entering the right parameters(only destination country)
        destination_country_id = self.flight.destination_country.id
        expected_flights = [self.flight]
        flights = Flight.get_flights_by_parameters(destination_country_id=destination_country_id)
        self.assertCountEqual(flights, expected_flights)


    def test_get_flights_by_parameters_success_only_with_departure_time(self):
        # Test if the method returns the flights as expected when entering the right parameters(only departure time)
        departure_time = datetime(2023,4,16,10,30, tzinfo=timezone.utc)
        expected_flights = [self.flight]
        flights = Flight.get_flights_by_parameters(departure_time=departure_time)
        self.assertEqual(flights[0], expected_flights[0])


    def test_get_flights_by_parameters_with_wrong_destination(self):
        # Test if the method doesn't return a flight that doesn't exist with wrong destination search input
        departure_time = datetime(2023,4,16,10,30, tzinfo=timezone.utc)
        origin_country_id = FlightModelTest.country
        destination_country_id = Country.objects.create(name="USA")
        with self.assertRaises(ObjectDoesNotExist):
            Flight.get_flights_by_parameters(origin_country_id, destination_country_id, departure_time)


    def test_get_flights_by_parameters_with_wrong_departure_time(self):
        # Test if the method doesn't return a flight that doesn't exist with wrong departure time search input
        departure_time = datetime(2023,5,16,10,30, tzinfo=timezone.utc)
        origin_country_id = FlightModelTest.country
        destination_country_id = self.flight.destination_country.id
        with self.assertRaises(ObjectDoesNotExist):
            Flight.get_flights_by_parameters(origin_country_id, destination_country_id, departure_time)


    def test_get_flights_by_parameters_with_wrong_origin_country(self):
        # Test if the method doesn't return a flight that doesn't exist with wrong origin country search input
        departure_time = datetime(2023,4,16,10,30, tzinfo=timezone.utc)
        origin_country_id = Country.objects.create(name='USA')
        destination_country_id = self.flight.destination_country.id
        with self.assertRaises(ObjectDoesNotExist):
            Flight.get_flights_by_parameters(origin_country_id, destination_country_id, departure_time)


    def test_get_flights_by_airline_id_success(self):
    # Test if the method return all the flights existing for the airline company with success
        expected_flights = [self.flight, self.another_flight]
        flights = Flight.get_flights_by_airline_id(FlightModelTest.airline_company.id)
        self.assertCountEqual(flights, expected_flights)


    def test_get_flights_by_airline_id_with_flightless_airline(self):
    # Test case if an airline have no flight, the method should return an empty list
        user = User.objects.create(username='no exist', password='password', email='nx@gmail.com', user_role='Airline Company')
        country = Country.objects.create(name='Israel')
        airline_company = AirlineCompany.objects.create(name='Ben Guryon Airline', country=country, user=user)
        with self.assertRaises(ObjectDoesNotExist):
            flights = Flight.get_flights_by_airline_id(airline_company.id)


    def test_get_flights_by_airline_id_with_invalid_airline_id(self):
    # Test case if there is no match between input id and existing airline company
        user = User.objects.create(username='no exist', password='password', email='nx@gmail.com', user_role='Airline Company')
        country = Country.objects.create(name='Israel')
        airline_company = AirlineCompany.objects.create(name='Ben Guryon Airline', country=country, user=user)
        airline_company.delete()
        with self.assertRaises(ObjectDoesNotExist):
            flights = Flight.get_flights_by_airline_id(airline_company.id)


    def test_get_flights_by_airline_id_with_multiple_airline_companies(self):
    # Test case for the method to return only the specific airline company flights in case there are multiple airline companies

        # create another airline company
        user = User.objects.create(username='no exist', password='password', email='nx@gmail.com', user_role='Airline Company')
        country = Country.objects.create(name='Israel')
        another_airline_company = AirlineCompany.objects.create(name='Ben Guryon Airline', country=country, user=user)

        # create flight that belong to the created airline
        another_flight = Flight.objects.create(
        airline_company = another_airline_company,
        origin_country = Country.objects.create(name='Moldova'),
        destination_country = Country.objects.create(name='Spain'),
        departure_time = datetime(2023,4,16,10,30, tzinfo=timezone.utc),
        landing_time = datetime(2023,4,16,10,30, tzinfo=timezone.utc) + timedelta(hours=6),
        remaining_tickets = 58
        )

        # Initiating the test
        expected_flights = [self.flight, self.another_flight]
        flights = Flight.get_flights_by_airline_id(FlightModelTest.airline_company.id)
        self.assertCountEqual(flights, expected_flights)

    def test_get_flights_by_airline_id_with_multiple_flights(self):
    # test that the method return all the flights airline have even if there is more then one flight
        airline_id = FlightModelTest.airline_company.id
        excepted_flights = [self.flight, self.another_flight]
        flights = Flight.get_flights_by_airline_id(airline_id)
        self.assertCountEqual(flights, excepted_flights)

    def test_get_flights_by_airline_id_with_multiple_flights_from_different_origin_and_destination_countries(self):
    # test that the method return all the flights airline have even if there is more then one flight
    # and the flight have different origin countries and different destinations countries
        airline_id = FlightModelTest.airline_company.id
        self.another_flight.origin_country = Country.objects.create(name='Fiji')
        excepted_flights = [self.flight, self.another_flight]
        flights = Flight.get_flights_by_airline_id(airline_id)
        self.assertCountEqual(flights, excepted_flights)


    def flight_that_landing_within_12_hours_from_now():
        departure_time = timezone.now()
        arriving_on_time_flight = Flight.objects.create(
            airline_company = FlightModelTest.airline_company,
            origin_country = Country.objects.create(name='Thailand'),
            destination_country = Country.objects.create(name='China'),
            departure_time = departure_time,
            landing_time = departure_time + timedelta(hours=6),
            remaining_tickets = 85
        )
        return arriving_on_time_flight
    

    def flight_that_landing_second_after_12_hours_from_now():
        departure_time = timezone.now()
        late_flight = Flight.objects.create(
            airline_company = FlightModelTest.airline_company,
            origin_country = Country.objects.create(name='Thailand'),
            destination_country = Country.objects.create(name='Finland'),
            departure_time = departure_time,
            landing_time = departure_time + timedelta(hours=12) + timedelta(seconds=10),
            remaining_tickets = 85
        )
        return late_flight
    
    def flight_that_landed_one_second_before_now():
        departure_time = timezone.now() - timedelta(hours=6)
        early_flight = Flight.objects.create(
            airline_company = FlightModelTest.airline_company,
            origin_country = Country.objects.create(name='Thailand'),
            destination_country = Country.objects.create(name='Finland'),
            departure_time = departure_time,
            landing_time = departure_time + timedelta(hours=5) + timedelta(minutes=59) + timedelta(seconds=59),
            remaining_tickets = 85
        )
        return early_flight


    def tests_def_get_arrival_flights_success_with_flight_landing_in_6_hours(self):
        """ test that the get arrival flights return successfully flight that supposed to land
        within the next 12 hours from the search time in a given country """
        expected_flight = FlightModelTest.flight_that_landing_within_12_hours_from_now()
        flight = Flight.get_arrival_flights(expected_flight.destination_country.id)
        self.assertEqual(flight[0], expected_flight)

 
    def  tests_def_get_arrival_flights_failure_with_flight_that_landing_in_12_hours_and_ten_second(self):
        """ test that the get arrival flights will not return flight that landing even
        second after 12 hours from the search time in a given country """
        flight = FlightModelTest.flight_that_landing_second_after_12_hours_from_now()
        country_id = flight.destination_country.id
        with self.assertRaises(ObjectDoesNotExist):
            flight=Flight.get_arrival_flights(country_id)


    def  tests_def_get_arrival_flights_failure_with_flight_that_landing_one_second_before_now(self):
        """ test that the get arrival flights will not return flight that landing even
        second before the search time in a given country """
        flight = FlightModelTest.flight_that_landed_one_second_before_now()
        country_id = flight.destination_country.id
        with self.assertRaises(ObjectDoesNotExist):
            flight=Flight.get_arrival_flights(country_id)



    def flight_that_departure_within_12_hours_from_now():
        departure_time = timezone.now() + timedelta(hours=2)
        departure_on_time_flight = Flight.objects.create(
            airline_company = FlightModelTest.airline_company,
            origin_country = Country.objects.create(name='Thailand'),
            destination_country = Country.objects.create(name='China'),
            departure_time = departure_time,
            landing_time = departure_time + timedelta(hours=6),
            remaining_tickets = 85
        )
        return departure_on_time_flight
    

    def flight_that_departure_second_after_12_hours_from_now():
        departure_time = timezone.now() + timedelta(hours=12) + timedelta(seconds=1)
        late_flight = Flight.objects.create(
            airline_company = FlightModelTest.airline_company,
            origin_country = Country.objects.create(name='Thailand'),
            destination_country = Country.objects.create(name='Finland'),
            departure_time = departure_time,
            landing_time = departure_time + timedelta(hours=12) + timedelta(seconds=10),
            remaining_tickets = 85
        )
        return late_flight
    
    def flight_that_departed_one_second_before_now():
        departure_time = timezone.now() - timedelta(seconds=1)
        early_flight = Flight.objects.create(
            airline_company = FlightModelTest.airline_company,
            origin_country = Country.objects.create(name='Thailand'),
            destination_country = Country.objects.create(name='Finland'),
            departure_time = departure_time,
            landing_time = departure_time + timedelta(hours=5) + timedelta(minutes=59) + timedelta(seconds=59),
            remaining_tickets = 85
        )
        return early_flight
    
    def test_get_departure_flights_success_with_flights_that_departure_inside_the_12_hours_range(self):
        """ test that get_departure_flights method return the expected flight if the flight
            departure withing the 12 hours range from the search time """
        expected_flight = FlightModelTest.flight_that_departure_within_12_hours_from_now()
        flight = Flight.get_departure_flights(expected_flight.origin_country.id)
        self.assertEqual(flight[0], expected_flight)


    def test_get_departure_flights_failure_with_flights_that_departure_after_the_12_hours_range(self):
        """ test that get_departure_flights method don't return flight if it
            departure after the 12 hours range from the search time """
        flight = FlightModelTest.flight_that_departure_second_after_12_hours_from_now()
        country_id = flight.origin_country.id
        with self.assertRaises(ObjectDoesNotExist):
            Flight.get_departure_flights(country_id)

    def test_get_departure_flights_failure_with_flights_that_departure_before_the_12_hours_range(self):
        """ test that get_departure_flights method don't return flight if it
            departure after the 12 hours range from the search time """
        flight = FlightModelTest.flight_that_departed_one_second_before_now()
        country_id = flight.origin_country.id
        with self.assertRaises(ObjectDoesNotExist):
            Flight.get_departure_flights(country_id)