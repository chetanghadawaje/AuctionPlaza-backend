import logging

from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from auction_plaza.utils.validation_error_utils import get_error_message_in_serializer
from bids.auctions_cache_utils import BidCaches
from bids.models import Bid, BidApply
from bids.serializers import BidSerializer, BidApplySerializer
from users.auth_utils import Authenticated

logger = logging.getLogger(__name__)


@api_view(['GET'])
def bid_polling(request, bid_id):
    """
    This api get all live details using redis or database when needed
    """
    # TODO insert data in cache for live
    live_user = BidCaches.live_user_count(bid_id)
    users_bids = BidCaches.get_list_of_bid(bid_id)
    data = [{"bids": users_bids, "live_user": live_user}]
    return Response({"Data": data, "Message": "Data fetched successfully", 'Status': status.HTTP_200_OK}, status=status.HTTP_200_OK)


class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.filter(is_active=True)
    serializer_class = BidSerializer
    http_method_names = ("get", "post")
    permission_classes = [Authenticated]

    def list(self, request, *args, **kwargs):
        if self.queryset:
            serializer = self.get_serializer(self.queryset, many=True)
            data, message, status_code = serializer.data, 'Bid data found.', status.HTTP_200_OK
        else:
            data, message, status_code = [], 'Bid data not found.', status.HTTP_404_NOT_FOUND

        return Response({"Data": data, "Message": message, 'Status': status_code}, status=status_code)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data, message, status_code = serializer.data, 'Bid created successfully', status.HTTP_201_CREATED
        except ValidationError:
            data, message, status_code = [], get_error_message_in_serializer(serializer), status.HTTP_400_BAD_REQUEST
            logger.warning(f"Validation Exception occurred for bid. Request data: {request.data} | Error Message: {message}")
        except Exception as _:
            logger.exception(f"Exception occurred in bid creation. Request data: {request.data}")
            data, message, status_code = [], 'Something went wrong', status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response({"Data": data, "Message": message, 'Status': status_code}, status=status_code)


class BidApplyViewSet(viewsets.ModelViewSet):
    queryset = BidApply.objects.filter(is_active=True)
    serializer_class = BidApplySerializer
    http_method_names = ("get", "post")
    permission_classes = [Authenticated]

    def list(self, request, *args, **kwargs):
        if self.queryset:
            serializer = self.get_serializer(self.queryset, many=True)
            data, message, status_code = serializer.data, 'Bid apply data found.', status.HTTP_200_OK
        else:
            data, message, status_code = [], 'Bid apply data not found.', status.HTTP_404_NOT_FOUND

        return Response({"Data": data, "Message": message, 'Status': status_code}, status=status_code)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # TODO abc replace bid id
            BidCaches.create_list_for_bids("abc", serializer.data.get('user'), serializer.data)
            data, message, status_code = serializer.data, 'Bid apply successfully', status.HTTP_201_CREATED
        except ValidationError:
            data, message, status_code = [], get_error_message_in_serializer(serializer), status.HTTP_400_BAD_REQUEST
            logger.warning(f"Validation Exception occurred for bid apply. Request data: {request.data} | Error Message: {message}")
        except Exception as _:
            logger.exception(f"Exception occurred in bid apply creation. Request data: {request.data}")
            data, message, status_code = [], 'Something went wrong', status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response({"Data": data, "Message": message, 'Status': status_code}, status=status_code)
