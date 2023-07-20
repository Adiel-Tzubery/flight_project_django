from django.db import models
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from datetime import datetime, timedelta
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.db.models import Q


# this file contain the flight management system's models. some of the models have method/s in here.


class Country(models.Model):
    name = models.CharField(max_length=80 , unique=True)
    flag = models.ImageField(
        null=True, blank=True, default='defaults/default_flag_piq.png', upload_to='countries/')


class Flight(models.Model):
    airline_company = models.ForeignKey(
        'AirlineCompany', on_delete=models.CASCADE, related_name='flights')
    origin_country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name='origin_country')
    destination_country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name='destination_country')
    departure_time = models.DateTimeField()
    landing_time = models.DateTimeField()
    remaining_tickets = models.IntegerField()
    price = models.IntegerField()

    def clean(self):
        if self.departure_time >= self.landing_time:
            raise ValidationError(
                'Landing time must be after the departure time.')

    @staticmethod
    def get_flights_by_parameters(origin_country_id=None, destination_country_id=None, date=None):
        """ return list of all the flights or reduce it according to conditions, if there is any. """

        # inserting all the existing conditions to a q.
        filter_conditions = Q()

        if origin_country_id is not None:
            filter_conditions &= Q(origin_country=origin_country_id)
        if destination_country_id is not None:
            filter_conditions &= Q(destination_country=destination_country_id)
        if date is not None:
            filter_conditions &= Q(departure_time__date=date)

        if not filter_conditions:  # if there are no conditions.
            try:
                flights = Flight.objects.all()
                if not flights.exists():  # if there are no flights.
                    raise ObjectDoesNotExist
                return flights
            except ObjectDoesNotExist:
                raise ObjectDoesNotExist('There are no flights.')

        # applying the conditions.
        try:
            flights = Flight.objects.filter(filter_conditions)
            if not flights.exists():  # if there are no flights.
                raise ObjectDoesNotExist
            return flights
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                'No flights found with the specified parameters.')

    @staticmethod
    def get_flights_by_airline_id(airline_id):
        """ return all flights of specific airline according to it's id. """

        try:  # get and return the flights.
            flights = Flight.objects.filter(airline_company_id=airline_id)
            if not flights.exists():  # if there are no flights.
                raise ObjectDoesNotExist
            else:
                return flights
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                f'There are no flights from airline {airline_id}.')

    @staticmethod
    def get_arrival_flights(country_id):
        """ return list of all flights that are arriving in the next 12 hours to specific country. """

        try:  # get and return the flights.
            flights = Flight.objects.filter(destination_country_id=country_id, landing_time__gte=datetime.now(
            ), landing_time__lte=datetime.now()+timedelta(hours=12))
            if not flights.exists():  # if there are no flights.
                raise ObjectDoesNotExist
            return flights
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                'No arriving flights in the next 12 hours.')

    @staticmethod
    def get_departure_flights(country_id):
        """ return list of all the flights that are departure in the next 12 hours from specific country. """

        try:
            flights = Flight.objects.filter(origin_country_id=country_id, departure_time__gte=datetime.now(
            ), departure_time__lte=datetime.now()+timedelta(hours=12))
            if not flights.exists():  # if there are no flights.
                raise ObjectDoesNotExist
            return flights
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                'No departing flight in the next 12 hours.')


class Ticket(models.Model):
    customer = models.ForeignKey(
        'Customer', on_delete=models.CASCADE, related_name='tickets')
    flight = models.ForeignKey(
        Flight, on_delete=models.CASCADE, related_name='tickets')

    class Meta:
        unique_together = ('flight', 'customer')

    @staticmethod
    def get_tickets_by_customer_id(customer_id):
        """ return list of all the customer's tickets. """

        try:  # getting the customer.
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:  # if customer does not exist in the system.
            raise ObjectDoesNotExist(
                f'No customer found with ID {customer_id}')

        try:  # get and return the tickets list.
            tickets = Ticket.objects.filter(customer=customer)
            if not tickets.exists():  # if there are no tickets.
                raise Ticket.DoesNotExist
            return tickets
        except Ticket.DoesNotExist:
            raise ObjectDoesNotExist(f'No tickets found for customer.')


class UserRole(models.Model):
    role_name = models.CharField(max_length=50, unique=True)
    group = models.OneToOneField(
        Group, blank=True, null=True, on_delete=models.CASCADE)


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, **kwargs):
        if not username:
            raise ValueError('The username field must be set')
        if not email:
            raise ValueError('The email field must be set')
        if not password:
            raise ValueError('The password field must be set')
        email = self.normalize_email(email)
        role = UserRole.objects.get(role_name=kwargs['user_role'])
        kwargs['user_role'] = role
        user = self.model(username=username, email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db) # save before assigning to group (user need to have id)
        user.groups.add(role.group) # assign to a group.
        return user

    def create_superuser(self, username, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    user_role = models.ForeignKey(
        UserRole, on_delete=models.SET_NULL, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    profile_pic = models.ImageField(
        null=True, blank=True, default='defaults/default_user_piq.jpeg', upload_to='users/')
    created = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    @staticmethod
    def get_user_by_username(username):
        """ return user according to it's username. """

        try:
            user = User.objects.filter(username=username)
            if not user.exists():
                raise ObjectDoesNotExist(f'No user found with username: {username}')
            return user
        except User.DoesNotExist:  # if user does not exist.
            raise ObjectDoesNotExist(f'No user found with username: {username}')

    @staticmethod
    def get_user_by_email(email):
        """ return user according to it's email. """

        try:
            user = User.objects.filter(email=email)
            if not user.exists():
                raise ObjectDoesNotExist(f'No user found with email: {email}.')    
            return user
        except User.DoesNotExist:
            raise ObjectDoesNotExist(f'No user found with email: {email}.')

    @property
    def get_user_role_name(self):
        return self.user_role.role_name


class Administrator(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='administrators')


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    credit_card_no = models.CharField(max_length=19, unique=True)
    phone_no = models.CharField(max_length=13, unique=True)
    address = models.TextField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='customers')

    @staticmethod
    def get_customer_by_username(username):
        """ return customer according to it's user's username. """

        try:
            customer = Customer.objects.select_related(
                'user').get(user__username=username)
            return customer
        except Customer.DoesNotExist:  # if customer does not exists.
            raise ObjectDoesNotExist(
                f'Customer with username {username} does not exist.')


class AirlineCompany(models.Model):
    name = models.CharField(max_length=50, unique=True)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name='airline_companies')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='airline_companies')

    @staticmethod
    def get_airline_by_username(username):
        """ return airline according to it's user's username. """

        try:
            airline = AirlineCompany.objects.select_related(
                'user').filter(user__username=username)
            return airline
        except AirlineCompany.DoesNotExist:  # if airline does not exists.
            raise ObjectDoesNotExist(
                f'Airline with username {username} does not exist.')

    @staticmethod
    def get_airline_by_name(name):
        """ return airline according to it's name. """
        try:
            airline = AirlineCompany.objects.filter(name=name)
            if not airline.exists():
                raise ObjectDoesNotExist
            return airline
        except AirlineCompany.DoesNotExist:
            raise ObjectDoesNotExist(f'Airline with name {name} does not exists.')
            


    @staticmethod
    def get_airlines_by_parameters(name=None, country_id=None):
        """ return list of all the airlines or reduce it according to conditions, if there is any. """

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
                if not airlines.exists():  # if there are no airlines.
                    raise ObjectDoesNotExist
            except ObjectDoesNotExist:
                raise ObjectDoesNotExist('There are no airlines')

        # applying the conditions
        try:
            airlines = AirlineCompany.objects.filter(filter_conditions)
            if not airlines.exists():  # if there are no airlines.
                raise ObjectDoesNotExist
            return airlines
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                'No airlines found with the specified parameters.')
