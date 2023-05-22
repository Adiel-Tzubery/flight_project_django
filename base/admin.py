from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from base.models import *

# Register your models here.
class CustomUser(UserAdmin):
    model = User


# myModels = [ Country, Flight, Ticket, UserRole, Administrator, Customer, AirlineCompany]
# admin.site.register(myModels)
# admin.site.register(User, CustomUser)

