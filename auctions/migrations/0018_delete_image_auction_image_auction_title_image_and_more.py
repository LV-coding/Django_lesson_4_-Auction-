# Generated by Django 4.0 on 2022-02-01 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_auctionbid'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Image',
        ),
        migrations.AddField(
            model_name='auction',
            name='image',
            field=models.ImageField(blank=True, default='', upload_to='images'),
        ),
        migrations.AddField(
            model_name='auction',
            name='title_image',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='auction',
            name='name',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='auction',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='auctions_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auctionswatchlist', to='auctions.auction'),
        ),
    ]