import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError

from users.serializers import UsersRegisterSerializer
from auction_plaza.utils.validation_error_utils import get_error_message_in_serializer
from users.models import Users
from users.jwt_utils import create_token


logger = logging.getLogger(__name__)


@api_view(['POST'])
def register(request):
    serializer = UsersRegisterSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data, message, status_code = serializer.data, 'User register successfully', status.HTTP_201_CREATED
    except ValidationError:
        data, message, status_code = [], get_error_message_in_serializer(serializer), status.HTTP_400_BAD_REQUEST
        logger.warning(f"Validation Exception occurred user register. Request data: {request.data} | Error Message: {message}")
    except Exception as _:
        logger.exception(f"Exception occurred in user register. Request data: {request.data}")
        data, message, status_code = [], 'Something went wrong', status.HTTP_500_INTERNAL_SERVER_ERROR

    return Response({"Data": data, "Message": message, 'Status': status_code}, status=status_code)


@api_view(['POST'])
def login(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        if email is None or password is None:
            raise ValidationError("Email and Password is requeue filed.")

        user = Users.objects.filter(is_active=True, email=email).first()
        if user is None:
            raise ValidationError("User not present.")
        elif not user.check_password(password):
            raise ValidationError("User password is not correct.")
        else:
            token_response = {"token": create_token(user)}
            data, message, status_code = [token_response], 'User login successfully', status.HTTP_200_OK
    except ValidationError as error:
        data, message, status_code = [], error.detail[0], status.HTTP_400_BAD_REQUEST
        logger.warning(f"Validation Exception occurred user login. Request data: {request.data} | Error Message: {message}")
    except Exception as _:
        logger.exception(f"Exception occurred in user login. Request data: {request.data}")
        data, message, status_code = [], 'Something went wrong', status.HTTP_500_INTERNAL_SERVER_ERROR

    return Response({"Data": data, "Message": message, 'Status': status_code}, status=status_code)
