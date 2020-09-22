from rest_framework import serializers
from .util import *

from django.utils import timezone

from accounts.models import Accounts
from .token_payload import *
expire = JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA']
print(expire)

class AccountSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    mobile = serializers.IntegerField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    gender = serializers.CharField(max_length=1, required=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    # expire = serializers.SerializerMethodField(read_only=True)
    # token = serializers.SerializerMethodField(read_only=True)
    token_response = serializers.SerializerMethodField(read_only=True)
    message = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Accounts
        fields = [
            'email',
            'mobile',
            'first_name',
            'last_name',
            'password'
            'password2',
            # 'expire',
            # 'token',
            'token_response',
            'message',
        ]

    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.get('password2')
        if p1 != p2:
            raise serializers.ValidationError("Password Mismatch")
        mobile = attrs.get('mobile')
        if len(str(mobile)) != 10:
            raise serializers.ValidationError("Incorrect Mobile Number")
        return attrs

    def get_message(self, obj):
        return "Thanks for registration"

    def create(self, validated_data):
        email = validated_data.get('email')
        mobile = validated_data.get('mobile')
        pasword = validated_data.get('password')
        account = Accounts.objects.create_user(email=email, mobile=mobile, password=pasword)
        account.first_name = validated_data.get('first_name')
        account.last_name = validated_data.get('last_name')
        account.gender = validated_data.get('gender')
        account.save()
        return account

    def get_email(self,obj):
        return self.first_name

    def get_last_name(self,obj):
        return self.last_name

    def validate_email(self,value):
        obj = Accounts.objects.filter(email__iexact=value)
        if obj.exists():
            raise serializers.ValidationError("Already Exist")
        return value

    def validate_mobile(self,value):
        obj = Accounts.objects.filter(mobile__iexact=value)
        if obj.exists():
            raise serializers.ValidationError("Already Exist")
        return value

    # def get_expire(self, obj):
    #     return expire + timezone.now()
    #
    # def get_token(self, obj):
    #     payload = jwt_payload_handler(obj)
    #     token = jwt_encode_handler(payload)
    #     return token

    def get_token_response(self, obj):
        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        response = custom_response_payload_handler(token,obj)
        return response