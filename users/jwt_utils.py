import datetime
import jwt

from django.conf import settings


def create_token(user):
    """
    Create token for user
    :user : user object
    """
    payload = {
        "id": user.id,
        "iat": datetime.datetime.now(),
        "exp": datetime.datetime.now() + datetime.timedelta(minutes=settings.JWT_EXP_MIN)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


def decode_token(token) -> dict:
    """
    decode token
    : token: token string
    """
    token_dict = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    return token_dict