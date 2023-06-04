from django.db import models
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from datetime import datetime, timedelta
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.db.models import Q

# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=30, unique=True)
    flag = models.ImageField(null=True, blank=True, default='defaults/default_flag_piq.png', upload_to='countries/')


class Flight(models.Model):
    airline_company= models.ForeignKey('AirlineCompany', on_delete=models.CASCADE, related_name='flights')
    origin_country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='origin_country')
    destination_country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='destination_country')
    departure_time = models.DateTimeField()
    landing_time = models.DateTimeField()
    remaining_tickets = models.IntegerField()
    price = models.IntegerField()


    def clean(self):
        if self.departure_time >= self.landing_time:
            raise ValidationError('Landing time must be after the departure time')
    

    @staticmethod
    def get_flights_by_parameters(origin_country_id=None, destination_country_id=None, date=None):
        """ method that get's all the flights according to parameters if there is any,
            if there isn't, the method will return all the flights, if there is any. """

        # inserting all the existing conditions to a q
        filter_conditions = Q()

        if origin_country_id is not None:
            filter_conditions &= Q(origin_country=origin_country_id)
        if destination_country_id is not None:
            filter_conditions &= Q(destination_country=destination_country_id)
        if date is not None:
            filter_conditions &= Q(departure_time__date=date)

        # if there are no conditions
        if not filter_conditions:
            try:
                flights = Flight.objects.all()
                if not flights.exists():
                    raise ObjectDoesNotExist
                return flights
            except ObjectDoesNotExist:
                raise ObjectDoesNotExist('There are no flights')
            
        # applying the conditions
        try:
            flights = Flight.objects.filter(filter_conditions)
            if not flights.exists():
                raise ObjectDoesNotExist
            return flights
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist('There are no flights matching the parameter/s')


    @staticmethod
    def get_flights_by_airline_id(airline_id):
        try:
            flights = Flight.objects.filter(airline_company_id=airline_id)
            if not flights.exists():
                raise ObjectDoesNotExist
            else:
                return flights
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f'There are no flights from airline {airline_id}')
        

    @staticmethod
    def get_arrival_flights(country_id):
        try:
            flights = Flight.objects.filter(destination_country_id=country_id, landing_time__gte=datetime.now(), landing_time__lte=datetime.now()+timedelta(hours=12))
            if not flights.exists():
                raise ObjectDoesNotExist
            return flights
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist('No arriving flights in the next 12 hours')
        

    @staticmethod
    def get_departure_flights(country_id):
        try:
            flights = Flight.objects.filter(origin_country_id=country_id, departure_time__gte=datetime.now(), departure_time__lte=datetime.now()+timedelta(hours=12))
            if not flights.exists():
                raise ObjectDoesNotExist
            return flights
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist('No departing flight in the next 12 hours')


class Ticket(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='tickets')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='tickets')

    class Meta:
        unique_together = ('flight', 'customer')


    @staticmethod
    def get_tickets_by_customer(customer_id):
        #getting the customer object if exists
        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            raise ObjectDoesNotExist(f'No customer found with ID {customer_id}')
        #getting the tickets, if there are any
        try:
            tickets = Ticket.objects.filter(customer=customer)
            if not tickets:
                raise Ticket.DoesNotExist
            return tickets
        except Ticket.DoesNotExist:
            raise ObjectDoesNotExist(f'No tickets found for customer {customer.first_name}')


class UserRole(models.Model):
    role_name = models.CharField(max_length=50, unique=True)
    group = models.OneToOneField(Group, blank=True, null=True, on_delete=models.CASCADE)


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, **kwargs):
        if not username:
            raise ValueError('The username field must be set')
        if not email:
            raise ValueError('The email field must be set')
        if not password:
            raise ValueError('The password field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('user_role', UserRole.objects.get(role_name='administrator'))
        return self.create_user(username, email, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    user_role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    profile_pic = models.ImageField(null=True, blank=True, default='defaults/default_user_piq.jpeg', upload_to='users/')
    created = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()


    @staticmethod
    def get_user_by_username(username):
        try:
            return User.objects.get(username=username)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f'No user found with username: {username}')


class Administrator(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='administrators')


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    credit_card_no = models.CharField(max_length=19, unique=True)
    phone_no = models.CharField(max_length=13, unique=True)
    address = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers')


    @staticmethod
    def get_customer_by_username(username):
        try:
            return Customer.objects.select_related('user').get(user__username=username)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f'Customer with username {username} does not exist')


class AirlineCompany(models.Model):
    name = models.CharField(max_length=50, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='airline_companies')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='airline_companies')

    @staticmethod
    def get_airline_by_username(username):
        try:
            return AirlineCompany.objects.select_related('user').get(user__username=username)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f'Airline with username {username} does not exist')


    @staticmethod
    def get_airlines_by_parameters(name=None, country_id=None):
        """ method that get's all the airlines according to parameters if there is any,
            if there isn't, the method will return all the airlines, if there is any. """
        # inserting all the existing conditions to a q
        filter_conditions = Q()

        if name is not None:
            filter_conditions &= Q(name=name)
        if country_id is not None:
            filter_conditions &= Q(country=country_id)

        # if there are no conditions
        if not filter_conditions:
            try:
                airlines = AirlineCompany.objects.all()
                if not airlines.exists():
                    raise ObjectDoesNotExist
            except ObjectDoesNotExist:
                raise ObjectDoesNotExist('There are no airlines')
            
        # applying the conditions
        try:
            airlines = AirlineCompany.objects.filter(filter_conditions)
            if not airlines.exists():
                raise ObjectDoesNotExist
            return airlines
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist('There are no airlines matching the parameter/s')