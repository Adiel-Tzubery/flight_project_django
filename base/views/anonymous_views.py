from facads.anonymous_facade import AnonymousFacade
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.serializers import UserModelSerializer, CustomerModelSerializer


def log_in(request):
    pass


@api_view(['POST'])
def create_new_user(request, **kwargs):
    try:
        user = AnonymousFacade.create_new_user(kwargs)
        serializer = UserModelSerializer(user, many=False)
        return Response(serializer.data)
    except Exception:
        raise Exception
    

@api_view(['POST'])
def add_customer(request, **kwargs):
    try:
        customer = AnonymousFacade.add_customer(kwargs)
        serializer = CustomerModelSerializer(customer, many=False)
        return Response(serializer.data)
    except Exception:
        raise Exception