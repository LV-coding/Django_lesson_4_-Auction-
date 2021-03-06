# Generated by Django 4.0 on 2022-01-31 16:55

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_remove_watchlist_auctions_list_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuctionBid',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_date_bid', models.DateTimeField(default=datetime.datetime.now)),
                ('price_bid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('auction_bid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auction_bid', to='auctions.auction')),
                ('author_bid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_bid', to='auctions.user')),
            ],
        ),
    ]
