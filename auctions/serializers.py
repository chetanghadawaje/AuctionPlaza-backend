from rest_framework import serializers

from auctions.models import Bid


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ('id', 'product', 'bidder', 'bid_amount', 'bid_time', 'bid_completed_flag')
        read_only_fields = ('id', 'bid_time', 'bid_completed_flag')
