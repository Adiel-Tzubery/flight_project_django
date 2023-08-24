from django.urls import path
from .views import base_views, administrator_views, anonymous_views, airline_views, customer_views


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [

    # auth views

    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # logout - located at base views, count as auth view.
    path('auth/logout/', base_views.log_out, name='log-out'),

    # Base views

    path('base/user_data/', base_views.get_user_data, name='user_data'),

    path('base/all-flights/', base_views.get_all_flights, name='all-flights'),
    path('base/flight/', base_views.get_flight_by_id, name='flight'),
    path('base/flights-by-parameters/',
         base_views.get_flights_by_parameters, name='flights-by-parameters'),

    path('base/all-airlines/', base_views.get_all_airlines, name='all-airlines'),
    path('base/airline/', base_views.get_airline_by_id, name='airline'),
    path('base/airlines-by-parameters/',
         base_views.get_airlines_by_parameters, name='airlines-by-parameter'),

    path('base/all-countries/', base_views.get_all_countries, name='countries'),
    path('base/country/', base_views.get_country_by_id, name='country'),

    # Administrator views

    path('adm/all-customers/', administrator_views.get_all_customers,
         name='all-customers'),

    path('adm/add-airline/', administrator_views.add_airline, name='add-airline'),
    path('adm/add-customer/', administrator_views.add_customer, name='add-customer'),
    path('adm/add-admin/', administrator_views.add_administrator, name='add-admin'),

    path('adm/remove-airline/', administrator_views.remove_airline,
         name='remove-airline'),
    path('adm/remove-customer/', administrator_views.remove_customer,
         name='remove-customer'),
    path('adm/remove-admin/', administrator_views.remove_administrator,
         name='remove=admin'),

    # Anonymous views

    # logout - located at base views, count as auth view. (line 20, this file.)

    # create_new_user does not need direct link to the FA.
    # it's been called from create_customer/airline/administrator methods(facades) directly.
#     path('ano/create-user/', anonymous_views.create_new_user, name='create-user'),
    path('ano/add-customer/', anonymous_views.add_customer, name='add-customer'),

    # Airline views

    path('airline/update-airline/',
         airline_views.update_airline, name='update-airline'),
    path('airline/add-flight/', airline_views.add_flight, name='add-flight'),
    path('airline/update-flight/',
         airline_views.update_flight, name='update=flight'),
    path('airline/remove-flight/',
         airline_views.remove_flight, name='remove_flight'),
    path('airline/my-flights/', airline_views.get_my_flights, name='my-flights'),

    # Customer views

    path('customer/update-customer/',
         customer_views.update_customer, name='update-customer'),
    path('customer/add-ticket/', customer_views.add_ticket, name='add-ticket'),
    path('customer/remove-ticket/',
         customer_views.remove_ticket, name='remove-ticket'),
    path('customer/my-tickets/',
         customer_views.get_my_tickets, name='my-tickets'),
]
