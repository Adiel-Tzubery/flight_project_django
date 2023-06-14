from django.urls import path
from .views import base_views

urlpatterns = [

    # facade base views

    path('all-flights/', base_views.get_all_flights, name='all-flights'),
    path('flight/<int:id>/', base_views.get_flight_by_id, name='flight'),
    path('flights-by-parameters/', base_views.get_flights_by_parameters, name='flights-by-parameters'),

    path('all-airlines/', base_views.get_all_airlines, name='all-airlines'),
    path('airline/<int:id>/', base_views.get_airline_by_id, name='airline'),
    path('airlines-by-parameters/', base_views.get_airlines_by_parameters, name='airlines-by-parameter'),

    path('countries/', base_views.get_all_countries, name='countries'),
    path('country/<int:id>/', base_views.get_country_by_id, name='country'),
]