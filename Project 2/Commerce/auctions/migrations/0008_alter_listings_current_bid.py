# Generated by Django 4.2.7 on 2023-12-08 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_listings_current_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='current_bid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
