import jwt
from django.conf import settings
from rest_framework_simplejwt.exceptions import InvalidToken

from .models import CustomUser


def get_user_id_from_token(token):
    try:
        # Decode the token using the secret key
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email = decoded_token['email']
        user = CustomUser.objects.get(email=email)
        return user.id
    except jwt.ExpiredSignatureError:
        raise InvalidToken('Token has expired')
    except jwt.InvalidTokenError:
        raise InvalidToken('Invalid token')
