import datetime
import jwt

from django.conf import settings
from rest_framework import exceptions


def create_token(user):
    """
    Create token for user
    :user : user object
    """
    try:
        payload = {
            "id": user.id,
            "exp": datetime.datetime.now() + datetime.timedelta(minutes=settings.JWT_EXP_MIN)
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return token
    except Exception as _:
        raise exceptions.AuthenticationFailed(_("Invalid token."))


def decode_token(token) -> dict:
    """
    decode token
    : token: token string
    """
    token_dict = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    return token_dict
