from django.urls import path

from auctions.views import bid_polling, BidViewSet

urlpatterns = [
    path("bid/polling/<str:id>", bid_polling),
    path("bid/create", BidViewSet.as_view({'get': 'list', 'post': 'create'}))
]
