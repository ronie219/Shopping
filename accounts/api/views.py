from django.contrib.auth import authenticate
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from accounts.api.serializer import AccountSerializer
from .token_payload import *


class AccountCreation(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = AccountSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if request.user.is_authenticated:
            return Response({"Msg": 'You already Login'}, status=200)
        email = request.data['email']
        pasword = request.data['password']
        account = authenticate(username=email, password=pasword)
        payload = jwt_payload_handler(account)
        token = jwt_encode_handler(payload)
        response = custom_response_payload_handler(token, user=account, request=request)
        return Response(response, status=200)
