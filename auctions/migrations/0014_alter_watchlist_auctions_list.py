# Generated by Django 4.0 on 2022-01-28 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_alter_watchlist_author_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='auctions_list',
            field=models.ManyToManyField(blank=True, related_name='auctionswatchlist', to='auctions.Auction'),
        ),
    ]
