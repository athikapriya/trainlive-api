from datetime import datetime
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from stations.models import Station
from trains.models import Train, TrainStation

from trains.data.load_data import TRAINS


def parse_timetable_time(value):

    if not value:
        return None

    value = str(value).strip().upper()

    value = value.replace("P.M.", "PM")
    value = value.replace("A.M.", "AM")
    value = value.replace("P M", "PM")
    value = value.replace("A M", "AM")

    for fmt in ("%I:%M %p", "%H:%M"):
        try:
            return datetime.strptime(value, fmt).time()
        except ValueError:
            pass

    raise CommandError(
        f"Invalid timetable value '{value}'. "
        "Expected format such as '04:30 PM'."
    )


def find_station(station_name):

    qs = Station.objects.filter(
        name_en__iexact=station_name
    ).order_by("id")

    matches = list(qs)

    if not matches:
        raise CommandError(
            f"Station name_en='{station_name}' was not found "
            "in the Stations table."
        )

    if len(matches) == 1:
        return matches[0]

    reference = matches[0]

    if reference.geom:
        nearby = []
        for station in matches:
            if not station.geom:
                continue

            distance = reference.geom.distance(
                station.geom
            )

            if distance <= 0.01:
                nearby.append(station)

        if len(nearby) == len(matches):
            return reference

    details = []

    for station in matches:
        if station.geom:
            details.append(
                f"id={station.id}, "
                f"lat={station.geom.y:.6f}, "
                f"lon={station.geom.x:.6f}"
            )
        else:
            details.append(
                f"id={station.id}, no geometry"
            )

    raise CommandError(
        f"Multiple distinct stations have "
        f"name_en='{station_name}': "
        + "; ".join(details)
        + ". The train data needs a unique station identifier "
          "or the station data needs to be corrected."
    )


class Command(BaseCommand):

    help = "Seed TrainLive trains and timetables"

    @transaction.atomic
    def handle(self, *args, **options):

        self.stdout.write("")
        self.stdout.write(
            self.style.WARNING(
                "Seeding TrainLive intercity trains..."
            )
        )
        self.stdout.write("")

        # =====================================================
        # Preflight station validation
        # =====================================================

        station_cache = {}
        validation_errors = []

        for train_data in TRAINS:

            for stop in train_data.get("stops", []):

                station_name = stop["station"]

                if station_name in station_cache:
                    continue

                try:
                    station_cache[station_name] = find_station(
                        station_name
                    )

                except CommandError as exc:
                    validation_errors.append(
                        str(exc)
                    )

        if validation_errors:

            self.stdout.write("")

            for error in validation_errors:
                self.stdout.write(
                    self.style.ERROR(
                        f"  - {error}"
                    )
                )

            self.stdout.write("")

            raise CommandError(
                "Station validation failed. "
                "No trains or timetables were changed."
            )

        # =====================================================
        # Seed trains
        # =====================================================

        created_trains = 0
        updated_trains = 0
        deleted_stops = 0
        created_stops = 0

        for train_data in TRAINS:

            train_number = str(
                train_data["number"]
            ).strip()

            train, created = Train.objects.update_or_create(
                number=train_number,

                defaults={
                    "name": train_data["name"],
                    "name_bn": train_data.get(
                        "name_bn",
                        "",
                    ),
                    "direction": train_data["direction"],
                    "off_day": train_data.get(
                        "off_day",
                        "",
                    ),
                    "is_active": True,
                },
            )

            if created:
                created_trains += 1
                action = "Created"
            else:
                updated_trains += 1
                action = "Updated"

            deleted_count, _ = TrainStation.objects.filter(
                train=train
            ).delete()

            deleted_stops += deleted_count

            stops = train_data.get("stops", [])

            if not stops:
                raise CommandError(
                    f"Train {train_number} has no timetable stops."
                )

            for stop_order, stop_data in enumerate(
                stops,
                start=1,
            ):

                station = station_cache[
                    stop_data["station"]
                ]

                arrival = parse_timetable_time(
                    stop_data.get("arrival")
                )

                departure = parse_timetable_time(
                    stop_data.get("departure")
                )

                TrainStation.objects.create(
                    train=train,
                    station=station,
                    stop_order=stop_order,
                    scheduled_arrival=arrival,
                    scheduled_departure=departure,
                )

                created_stops += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"{action}: "
                    f"{train.number} - "
                    f"{train.name} "
                    f"({len(stops)} stops)"
                )
            )

        # =====================================================
        # Summary
        # =====================================================

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Created trains: {created_trains}"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Updated trains: {updated_trains}"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Deleted old timetable stops: {deleted_stops}"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Created timetable stops: {created_stops}"
            )
        )
        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "TrainLive train seeding completed successfully."
            )
        )
