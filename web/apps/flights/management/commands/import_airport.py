import json

from django.core.management.base import BaseCommand

from apps.flights.models import Airport


class Command(BaseCommand):
    help = "Import airports from a data file"

    def handle(self, *args, **kwargs):
        with open(
            "apps/flights/data/airports.json", newline="", encoding="utf-8"
        ) as json_data:
            data = json.load(json_data)
            for airport in data:
                Airport.objects.create(
                    name=airport["name"],
                    city=airport["city"],
                    country=airport["country"],
                    iata=airport["iata"] if airport["iata"] != "\\N" else None,
                    icao=airport["icao"],
                    latitude=airport["latitude"],
                    longitude=airport["longitude"],
                    altitude=airport["altitude"],
                    timezone_offset=airport["timezone_offset"]
                    if airport["timezone_offset"] != "\\N"
                    else None,
                    dst=airport["dst"],
                )
                self.stdout.write(
                    self.style.SUCCESS(f'{airport["name"]} was created')
                )

        self.stdout.write(self.style.SUCCESS("Successfully imported airports"))
