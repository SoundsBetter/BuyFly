# Generated by Django 5.0.3 on 2024-03-18 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0011_booking_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
    ]
