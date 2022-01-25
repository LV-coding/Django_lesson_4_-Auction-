from dataclasses import fields
from django import forms

from .models import Auction, Image, Comment

class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ('name', 'price', 'about', 'category',  )

class AuctionComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text_comment', )