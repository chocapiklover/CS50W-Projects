from django.contrib.auth.models import AbstractUser
from django.db import models, migrations
from django.utils import timezone


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.categoryName

class listings(models.Model):
    title = models.CharField(max_length=55)
    description = models.TextField(max_length=320)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    highest_bidder = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='highest_bidder')
    image_url = models.URLField(blank=True, null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    status = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    watchlist = models.ManyToManyField(User, related_name='watchlist', blank=True)

    
    def __str__(self):
        return self.title

class BidHistory(models.Model):
    listing = models.ForeignKey(listings, on_delete=models.CASCADE, related_name='bid_history')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bidder')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def bid_amount(self):
        return self.listing.starting_bid

    def __str__(self):
        return f"Bid by {self.user.username} on {self.listing.title}"



class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenter')
    comments = models.TextField(max_length=255, blank=True)
    listing = models.ForeignKey(listings, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'{self.user.username} {self.comments}'
