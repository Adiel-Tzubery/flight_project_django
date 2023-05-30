from django.test import TestCase
from base.models import User, Country, AirlineCompany, UserRole
from django.core.exceptions import ObjectDoesNotExist


class AirlineCompaniesModelTests(TestCase):

    def setUp(self):
        """ creating a test airline_companies user object. """
        self.user_role = UserRole.objects.create(role_name='airline_company')
        self.country = Country.objects.create(name = 'Israel')
        self.user = User.objects.create_user(username = 'Ben-Guryon', email = 'bg@gmail.com', password = 'password', user_role = self.user_role)
        self.airline_company = AirlineCompany.objects.create(name = 'Ben-Guryon_airport', country=self.country, user=self.user)


    def test_get_airline_by_username_success(self):
        """  Test that the method returns the airline_company user object for an existing one """
        airline_company = self.airline_company.get_airline_by_username(username='Ben-Guryon')
        self.assertEqual(airline_company.user.username , 'Ben-Guryon')


    def test_get_airline_by_username_failure(self):
        """ Test that the method don't returns airline_company user object for a non existing user. """
        with self.assertRaises(ObjectDoesNotExist):
           self.airline_company.get_airline_by_username(username='la-guardia')

    
    def test_get_airline_by_username_failure_with_only_one_key_wrong(self):
        """ Test that the method don't returns airline_company user object for a non existing user. """
        with self.assertRaises(ObjectDoesNotExist):
           self.airline_company.get_airline_by_username(username='Ben-Guryob')
