from dataclasses import fields
from django import forms

from .models import Auction,  Comment, AuctionBid

class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ('name', 'price', 'about', 'category', 'title_image', 'image', )

class AuctionComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text_comment', )

class AuctionBidForm(forms.ModelForm):
    class Meta:
        model = AuctionBid
        fields = ('price_bid', )
""""
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'image')
"""