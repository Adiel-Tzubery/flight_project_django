from django.test import TestCase
from base.models import User, Administrator
from django.core.exceptions import ObjectDoesNotExist



class UserModelTests(TestCase):

    def setUp(self):
        """ creating a test user object. """
        self.user = User.objects.create(username='shalomlecha', password='password', email='shalom@gmail.com', user_role='Administrator')
        self.administrator = Administrator.objects.create(first_name='shalom', last_name='lecha', user=self.user)
        
    
    def test_get_user_by_username_success(self):
        """ Test that the method returns user object for an existing one. """
        user = self.administrator.user.get_user_by_username(username='shalomlecha')
        self.assertEqual(user.username, 'shalomlecha')


    def test_get_user_by_username_failure_with_only_one_key_wrong(self):
        """ Test that the method don't returns user object for a non existing user
        even if only one key is wrong. """
        with self.assertRaises(ObjectDoesNotExist):
            self.administrator.user.get_user_by_username(username='shalomleche')



