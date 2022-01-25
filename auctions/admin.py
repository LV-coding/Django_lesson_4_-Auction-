from django.contrib import admin
from .models import User, Auction, Comment

admin.site.register(User)
admin.site.register(Auction)
admin.site.register(Comment)
