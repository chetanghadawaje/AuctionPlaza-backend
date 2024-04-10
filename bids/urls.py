from django.urls import path

from bids.views import bid_polling, BidViewSet, BidApplyViewSet

urlpatterns = [
    path("polling/<str:bid_id>", bid_polling),
    path("", BidViewSet.as_view({'get': 'list', 'post': 'create'})),
    path("apply", BidApplyViewSet.as_view({'get': 'list', 'post': 'create'}))
]
