import logging

from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend

from auction_plaza.utils.validation_error_utils import get_error_message_in_serializer
from bids.models import Bid, BidApply
from bids.serializers import BidSerializer, BidApplySerializer

logger = logging.getLogger(__name__)


def bid_polling(request, id):
    """
    This api get all live details using redis or database when needed
    """
    pass


class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.filter(is_active=True)
    serializer_class = BidSerializer
    http_method_names = ("get", "post")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product', 'bidder', 'bid_completed_flag']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_expection=True)
            serializer.save()
            data, message, status_code = serializer.data, 'Bid created successfully', status.HTTP_201_CREATED
        except ValidationError:
            data, message, status_code = [], get_error_message_in_serializer(serializer), status.HTTP_400_BAD_REQUEST
            logger.warning(f"Validation Exception occurred. Request data: {request.data} | Error Message: {message}")
        except Exception as _:
            logger.exception(f"Exception occurred in bid creation. Request data: {request.data}")
            data, message, status_code = [], 'Something went wrong', status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response({"Data": data, "Message": message, 'Status': status_code}, status=status_code)


class BidApplyViewSet(viewsets.ModelViewSet):
    queryset = BidApply.objects.filter(is_active=True)
    serializer_class = BidApplySerializer
    http_method_names = ("get", "post")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product', 'user']

