# Generated by Django 4.2.7 on 2023-12-08 21:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_listings_current_bid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listings',
            name='current_bid',
        ),
    ]