from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
from django.conf import settings

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    pass

class Auction(models.Model):
    id = models.AutoField(primary_key=True)
    category_choices = (
        ("sports", "sports"),
        ("books", "books"),
        ("other", "other"),
        ("games", "games"),
        ("lazy ass", "Im too lazy for that")
    )
    name = models.CharField(max_length=32)
    category = models.CharField(max_length=15, choices=category_choices, default="LA")
    price = models.DecimalField(decimal_places=2, max_digits=10)
    about = models.TextField()
    created_date = models.DateTimeField(default=datetime.datetime.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'{self.name}___with price___{self.price}$;'