from rest_framework import serializers

from bids.models import Bid, BidApply


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ('id', 'product', 'bid_amount', 'bid_time', 'bid_completed_flag')
        read_only_fields = ('id', 'bid_time', 'bidder', 'bid_completed_flag')


class BidApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = BidApply
        fields = ('id', 'product', 'user')
        read_only_fields = ('id', 'user')
