from django.contrib import admin
from .models import User, listings, Category, BidHistory, Comments


class BidHistoryAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'bid_amount', 'created_at')
    list_filter = ('listing', 'user')
    search_fields = ('listing__title', 'user__username')
    ordering = ('-created_at',) 

class BidHistoryInline(admin.TabularInline):
    model = BidHistory
    extra = 0

class ListingsAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'starting_bid', 'highest_bidder_info', 'seller', 'status', 'category', 'watchlist_count')
    search_fields = ('title', 'seller__username')
    list_filter = ('status', 'category')
    filter_horizontal = ('watchlist',)
    inlines = [BidHistoryInline]

    
    def highest_bidder_info(self, obj):
        return f"{obj.highest_bidder.username} ({obj.highest_bidder.email})" if obj.highest_bidder else "No bids yet"
    highest_bidder_info.short_description = 'Highest Bidder'

    def latest_bid(self):
        latest_bid = self.bid_history.last()
        if latest_bid:
            return f"{latest_bid.user.username}: {latest_bid.bid_amount}"
        return "No bids yet"

    def watchlist_count(self, obj):
        return obj.watchlist.count()
    watchlist_count.short_description = 'Watchlist Count'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        # Fetch the object with additional details
        listing = self.get_object(request, object_id)
        # Add any additional details to the context
        extra_context = extra_context or {}
        extra_context['additional_details'] = {
            'custom_detail': 'This is a custom detail for the listing.',
            # Add more details as needed
        }
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    latest_bid.short_description = 'Latest Bid'




# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(listings, ListingsAdmin) 
admin.site.register(Comments)
admin.site.register(BidHistory, BidHistoryAdmin)
