from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    pass

class Auction(models.Model):
    id = models.AutoField(primary_key=True)
    category_choices = (
        ("SP", "sports"),
        ("BO", "books"),
        ("OT", "other"),
        ("GA", "games"),
        ("LA", "Im too lazy for that")
    )
    name = models.CharField(max_length=32)
    category = models.CharField(max_length=2, choices=category_choices, default="LA")
    price = models.DecimalField(decimal_places=2, max_digits=10)
    about = models.TextField()
    created_date = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return f'{self.name}___with price___{self.price}$;'