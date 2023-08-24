from facads.anonymous_facade import AnonymousFacade
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from base.serializers import  CustomerModelSerializer



@api_view(['POST'])
@permission_classes([AllowAny])
def add_customer(request):
    
    try:
        customer = AnonymousFacade.add_customer(
            username=request.data['username'],
            email=request.data['email'],
            password=request.data['password'],
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
            credit_card_no=request.data['credit_card_no'],
            phone_no=request.data['phone_no'],
            address=request.data['address'],
            user_role=request.data['user_role'],
        )
        serializer = CustomerModelSerializer(customer, many=False)
        return Response(serializer.data)
    except Exception as e:
        return Response({'Error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# possibly redundant api view (not been called directly from the FA).
# stay here only for te requirements.
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def create_new_user(request, **kwargs):
#     """ get new user, serialize it and return it's data. """

#     try:
#         user = AnonymousFacade.create_new_user(kwargs)
#         serializer = UserModelSerializer(user, many=False)
#         return Response(serializer.data)
#     except Exception as e:
#         return Response({'Error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)