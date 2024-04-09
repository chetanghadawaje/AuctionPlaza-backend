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
        product_obj = data.get('product')
        if product_obj is None:
            raise serializers.ValidationError("Product not present for Bid.")
        elif product_obj.status == 'completed':
            raise serializers.ValidationError("Product auction close.")
        elif product_obj.status == 'upcoming':
            raise serializers.ValidationError("Product auction not yet start.")
        elif product_obj.initial_price >= data.get("bid_amount"):
            raise serializers.ValidationError("Product initial price is greater than your bid amount.")
        return data


class BidApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = BidApply
        fields = ('id', 'product', 'user')
        read_only_fields = ('id', )

    def validate(self, data):
        product_obj = data.get('product')
        if product_obj.status != 'upcoming':
            raise serializers.ValidationError("Product auction now closed.")
        elif product_obj.user == data.get('user'):
            raise serializers.ValidationError("You are not eligible for this bid.")
        bid_apply_obj = BidApply.objects.filter(is_active=True, user=data.get('user'), product=product_obj)
        if bid_apply_obj:
            raise serializers.ValidationError("Already apply for this bid.")
        return data
