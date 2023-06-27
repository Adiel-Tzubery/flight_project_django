from facads.anonymous_facade import AnonymousFacade
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from base.serializers import UserModelSerializer, CustomerModelSerializer
from django.core.exceptions import PermissionDenied, ValidationError


# def log_in(request, username, password):
#     """ login view: accept - request, username and password. """

#     try: # log in the user and returning the authenticated user in json format.
#         user = AnonymousFacade.log_in(request, username, password)
#         serializer = UserModelSerializer(user, many=False)
#         return Response(serializer.data)
#     except (PermissionDenied, ValidationError): # error handling.
#         return Response({"error": "Invalid username or password."}, status=status.HTTP_400_BAD_REQUEST)
#     except Exception:
#         return Response({"error": "An unexpected error occurred during login."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def create_new_user(request, **kwargs):
    """ create new user view. """

    try: # creating new user and returning it in json format.
        user = AnonymousFacade.create_new_user(kwargs)
        serializer = UserModelSerializer(user, many=False)
        return Response(serializer.data)
    except Exception as e: # error handling.
        return Response({f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
def add_customer(request, **kwargs):
    """ create new customer view. """

    try: # creating new customer user and returning it in json format.
        customer = AnonymousFacade.add_customer(kwargs)
        serializer = CustomerModelSerializer(customer, many=False)
        return Response(serializer.data)
    except Exception as e: # error handling.
        return Response({f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)