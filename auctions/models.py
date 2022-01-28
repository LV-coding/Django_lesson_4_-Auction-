from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
from django.conf import settings

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    pass


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.title


class Auction(models.Model):
    id = models.AutoField(primary_key=True)
    category_choices = (
        ("sports", "sports"),
        ("books", "books"),
        ("other", "other"),
        ("games", "games")
    )
    name = models.CharField(max_length=64)
    category = models.CharField(max_length=15, choices=category_choices, default="other")
    price = models.DecimalField(decimal_places=2, max_digits=10)
    about = models.TextField()
    created_date = models.DateTimeField(default=datetime.datetime.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  #settings.AUTH_USER_MODEL
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}___with price___{self.price}$;'
    

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    author_comment = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_comment")  #settings.AUTH_USER_MODEL
    auction_comment = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="auction_comment")
    created_date_comment = models.DateTimeField(default=datetime.datetime.now)
    text_comment = models.TextField()

    def __str__(self):
        return f'{self.author_comment}___{self.auction_comment}__{self.created_date_comment}'

class Watchlist(models.Model):
        id = models.AutoField(primary_key=True)
        author_watchlist = models.ForeignKey(User, on_delete=models.CASCADE, related_name="authorswatchlist")
        auctions_list = models.ManyToManyField(Auction,  blank=True, related_name="auctionswatchlist")

        def __str__(self):
            return f'{self.auctions_list}'