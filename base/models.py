from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group

# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=30, unique=True)
    flag = models.ImageField(null=True, blank=True, default='defaults/default_flag_piq.png', upload_to='countries/')


class Flight(models.Model):
    airline_company_id = models.ForeignKey('AirlineCompany', on_delete=models.CASCADE)
    origin_country_id = models.ForeignKey(Country, related_name='origin_country', on_delete=models.CASCADE)
    destination_country_id = models.ForeignKey(Country, related_name='destination_country', on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    landing_time = models.DateTimeField()
    remaining_tickets = models.IntegerField()
    price = models.IntegerField()

class Ticket(models.Model):
    customer_id = models.ForeignKey('Customer', on_delete=models.CASCADE)
    flight_id = models.ForeignKey(Flight, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('flight_id', 'customer_id')


class UserRole(models.Model):
    role_name = models.CharField(max_length=50, unique=True)
    # group = models.OneToOneField(Group, blank=True, null=True, on_delete=models.CASCADE)


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not password:
            raise ValueError('The password field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_role', UserRole.objects.get(role_name='admin'))
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    user_role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    thumbnail = models.ImageField(null=True, blank=True, default='defaults/default_user_piq.jpeg', upload_to='users/')
    created = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()


class Administrator(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    credit_card_no = models.CharField(max_length=16, unique=True)
    phone_no = models.CharField(max_length=10 ,unique=True)
    address = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class AirlineCompany(models.Model):
    name = models.CharField(max_length=50, unique=True)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)