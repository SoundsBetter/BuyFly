# Generated by Django 5.0.3 on 2024-03-18 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0009_ticket_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketoption',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
    ]
