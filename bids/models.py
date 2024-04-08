from datetime import datetime

from django.db import models

from auction_plaza.utils.models_utils import BaseModelLog
from users.models import Users
from products.models import Product


class Bid(BaseModelLog):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    bidder = models.ForeignKey(Users, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    bid_completed_flag = models.BooleanField(default=False)

    def __str__(self):
        return f"Bid for {self.product} by {self.bidder} at {self.bid_time}"

    def save(self, *args, **kwargs):
        if not self.bidder:
            self.bidder = request.user
        if not self.bid_time:
            self.bid_time = datetime.now()
        if not self.ip_address:
            self.ip_address = request.META['REMOTE_ADDR']
        super().save(*args, **kwargs)


class BidApply(BaseModelLog):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Bid application by User ID: {self.user.id} for Product ID: {self.product.id}"