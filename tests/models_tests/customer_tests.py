from django.test import TestCase
from base.models import User, Customer, UserRole
from django.core.exceptions import ObjectDoesNotExist



class CustomerModelTests(TestCase):

    def setUp(self):
        """ creating a test customer object. """
        self.user_role = UserRole.objects.create(role_name='Customer')
        self.user = User.objects.create_user(username='adieltzu', password='password', email='shalom@gmail.com', user_role=self.user_role)
        self.customer = Customer.objects.create(first_name='Adiel',
                                                last_name='Tzubery',
                                                address='Kfar-Hasidim',
                                                phone_no='056-9856925',
                                                credit_card_no='0452-0527-9856-9874',
                                                user=self.user)


    def test_get_customer_by_username_success(self):
        """ Test that the method returns customer object for an existing one. """
        customer = self.customer.get_customer_by_username(username='adieltzu')
        self.assertEqual(customer.user.username, 'adieltzu')


    def test_get_customer_by_username_failure(self):
        """ Test that the method don't returns customer object for a non existing user. """
        with self.assertRaises(ObjectDoesNotExist):
            self.customer.get_customer_by_username(username='adi')


    def test_get_customer_by_username_failure_with_only_one_key_wrong(self):
        """ Test that the method don't returns customer object for a non existing user. """
        with self.assertRaises(ObjectDoesNotExist):
            self.customer.get_customer_by_username(username='adieltzv')