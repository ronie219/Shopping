from django.utils import timezone
from rest_framework_jwt.settings import api_settings


from .util import JWT_AUTH

expire = JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA']
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def custom_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': user.email,
        'expire_on': timezone.now() + expire
    }
