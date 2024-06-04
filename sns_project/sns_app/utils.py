from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.conf import settings
from .models import CustomUser
import jwt

def get_user_id_from_token(token):
    try:
        # Decode the token using the secret key
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email = decoded_token['email']
        user=CustomUser.objects.get(email=email)
        return user.id
    except jwt.ExpiredSignatureError:
        raise InvalidToken('Token has expired')
    except jwt.InvalidTokenError:
        raise InvalidToken('Invalid token')
