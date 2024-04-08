from datetime import datetime

from rest_framework import serializers

from bids.models import Bid, BidApply
from products.models import Product


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ('id', 'product', 'bidder', 'bid_amount', 'bid_time', 'bid_completed_flag')
        read_only_fields = ('id', 'bid_time', 'bid_completed_flag')

    def validate(self, data):
        product_obj = Product.objects.filter(is_active=True, product=data.get('product'))
        if product_obj is None:
            raise serializers.ValidationError("Product not present for Bid.")
        elif product_obj.status == 'completed':
            raise serializers.ValidationError("Product auction close.")
        elif product_obj.status == 'upcoming' or product_obj.auction_date_time < datetime.now():
            raise serializers.ValidationError("Product auction not yet start.")
        elif product_obj.initial_price >= data.get("bid_amount"):
            raise serializers.ValidationError("Product auction yet not start.")


class BidApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = BidApply
        fields = ('id', 'product', 'user')
        read_only_fields = ('id', )

    def validate(self, data):
        bid_apply_obj = BidApply.objects.filter(is_active=True, user=data.get('user'), product=data.get('product'))
        if bid_apply_obj:
            raise serializers.ValidationError("Already apply for this bid.")
        return data
