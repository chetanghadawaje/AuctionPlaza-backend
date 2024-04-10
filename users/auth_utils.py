import datetime
import logging

from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated

from users.jwt_utils import decode_token
from users.models import Users

logger = logging.getLogger(__name__)


class Authenticated(IsAuthenticated):

    def has_permission(self, request, view):
        token = request.headers.get("Authorization")
        if token is None:
            raise exceptions.AuthenticationFailed(detail="Token not present")
        else:
            token = token.split(" ")[1]
            token_data_dict = decode_token(token)
            if token_data_dict.get("exp") < datetime.datetime.now().timestamp():
                raise exceptions.AuthenticationFailed(detail="Token expired")
            if token_data_dict.get("id"):
                user_obj = Users.objects.filter(pk=token_data_dict.get("id")).first()
                if user_obj is None:
                    raise exceptions.AuthenticationFailed(detail="User not found")
                request.session['user_id'] = user_obj.id
            return True
