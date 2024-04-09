import logging

from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from users.jwt_utils import decode_token

logger = logging.getLogger(__name__)


class Authenticated(IsAuthenticated):

    def has_permission(self, request, view):
        try:
            token = request.headers.get("Authorization")
            if token is None:
                raise exceptions.AuthenticationFailed(detail=_("Token not present"))
            else:
                token_data_dict = decode_token(token)
                return True
        except:
            logger.exception(f"Exception occurred during token validated")
            exceptions.NotAuthenticated()
