# Generated by Django 5.0.3 on 2024-03-14 13:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AirplaneType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=32, unique=True)),
                ('params', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('city', models.CharField(blank=True, max_length=32, null=True)),
                ('country', models.CharField(max_length=32)),
                ('iata', models.CharField(max_length=5, null=True, unique=True)),
                ('icao', models.CharField(max_length=7, null=True, unique=True)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=10)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=10)),
                ('altitude', models.IntegerField()),
                ('timezone_offset', models.FloatField(blank=True, null=True)),
                ('dst', models.CharField(choices=[('E', 'Europe'), ('A', 'Us Canada'), ('S', 'South America'), ('O', 'Australia'), ('Z', 'New Zealand'), ('U', 'Unknown')], default='U', max_length=2, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Airplane',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=16, unique=True)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='airplane', to='flights.airplanetype')),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrival_airport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrivals', to='flights.airport')),
                ('departure_airport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departures', to='flights.airport')),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('scheduled', 'Scheduled'), ('on_time', 'On Time'), ('delayed', 'Delayed'), ('boarding', 'Boarding'), ('departed', 'Departed'), ('in_flight', 'In Flight'), ('landed', 'Landed'), ('cancelled', 'Cancelled'), ('diverted', 'Diverted'), ('completed', 'Completed')], default='scheduled', max_length=10)),
                ('number', models.CharField(max_length=10)),
                ('departure_datetime', models.DateTimeField()),
                ('arrival_datetime', models.DateTimeField()),
                ('base_price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('options_price_coefficient', models.DecimalField(decimal_places=5, max_digits=20)),
                ('options', models.ManyToManyField(blank=True, to='bookings.option')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flights', to='flights.route')),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10)),
                ('seat_type', models.CharField(choices=[('Economy', 'E'), ('Business', 'B')], max_length=32)),
                ('airplane', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seats', to='flights.airplane')),
            ],
        ),
        migrations.AddConstraint(
            model_name='route',
            constraint=models.UniqueConstraint(fields=('departure_airport', 'arrival_airport'), name='unique_route'),
        ),
    ]
