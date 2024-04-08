from django.contrib import admin

from bids.models import Bid, BidApply


class BidAdmin(admin.ModelAdmin):
    list_display = ('product', 'bidder', 'bid_amount', 'bid_time')
    list_filter = ('product', 'bidder', 'bid_completed_flag')


admin.site.register(Bid, BidAdmin)


class BidApplyAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')


admin.site.register(BidApply, BidApplyAdmin)
