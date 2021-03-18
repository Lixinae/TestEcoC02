import sys

from django.apps import AppConfig


class AppDjangoConfig(AppConfig):
    name = "app"
    verbose_name = "Django test technique EcoC02"

    @staticmethod
    def grab_data_and_save_to_db():
        # Pose soucis si la DB n'est pas initialisé et que les tables n'existe pas à ce moment
        from app.models import RealDataC02, FilteredDataC02
        from app.data.data_fetcher import grab_data_from_api, filter_co2_data_to_one_hour_frequence, \
            convert_date_time_to_timestamp

        co2_data_fetched = grab_data_from_api("2017-01-01T00:00:00", "2018-12-31T23:00:00")
        filtered_data = filter_co2_data_to_one_hour_frequence(co2_data_fetched)

        co2_data_fetched = [{
            'datetime': convert_date_time_to_timestamp(x["datetime"]),
            'co2_rate': x["co2_rate"]
        } for x in co2_data_fetched]
        filtered_data = [{
            'datetime': convert_date_time_to_timestamp(x["datetime"]),
            'co2_rate': x["co2_rate"]
        } for x in filtered_data]

        print("Initiliazing DB with Data from API")
        co2_data_fetched_to_insert = [
            RealDataC02(datetime=data["datetime"], co2_rate=data["co2_rate"]) for data in co2_data_fetched
        ]
        try:
            RealDataC02.objects.bulk_create(co2_data_fetched_to_insert)
        except ValueError:
            RealDataC02.objects.bulk_update(co2_data_fetched_to_insert)
        print("Finished initiliazing DB with Data from API")
        print("Setting up table data for filtered data")
        filtered_data_to_insert = [
            FilteredDataC02(datetime=data["datetime"], co2_rate=data["co2_rate"]) for data in filtered_data
        ]
        try:
            FilteredDataC02.objects.bulk_create(filtered_data_to_insert)
        except ValueError:
            FilteredDataC02.objects.bulk_update(filtered_data_to_insert)
        print("Setup for filtered data finished")
        pass

    def ready(self):
        # On ne veut executer que lorsque l'on lance le serveur, pas sur des migrate, makemigrations ou autre
        if 'runserver' in sys.argv:
            self.grab_data_and_save_to_db()
