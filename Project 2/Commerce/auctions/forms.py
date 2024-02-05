from django import forms
from .models import listings

class ListingForm(forms.ModelForm):
    class Meta:
        model = listings
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']