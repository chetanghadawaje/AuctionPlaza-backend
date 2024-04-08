from django.db import models
from auction_plaza.utils.models_utils import BaseModelLog

from users.models import Users
from products.models import Product


class Bid(BaseModelLog):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    bidder = models.ForeignKey(Users, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    bid_completed_flag = models.BooleanField(default=False)

    def __str__(self):
        return f"Bid for {self.product} by {self.bidder} at {self.bid_time}"


class BidApply(BaseModelLog):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Bid application by User ID: {self.user.id} for Product ID: {self.product.id}"