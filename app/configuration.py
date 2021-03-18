from django.apps import AppConfig


class AppDjangoConfig(AppConfig):
    name = "app"
    verbose_name = "Django test technique EcoC02"

    def ready(self):
        from app.models.models import RealDataC02, FilteredDataC02
        from app.data.data_fetcher import grab_data_from_api, filter_co2_data_to_one_hour_frequence

        co2_data_fetched = grab_data_from_api("2017-01-01T00:00:00", "2018-12-31T00:00:00")
        filtered_data = filter_co2_data_to_one_hour_frequence(co2_data_fetched)
        for data in co2_data_fetched:
            datetime_split = data["datetime"].split("T")
            print(datetime_split)
            real_data_co2 = RealDataC02(date=datetime_split[0], time=datetime_split[1], co2_rate=data["co2_rate"])
            real_data_co2.save()
        for data in filtered_data:
            datetime_split = data["datetime"].split("T")
            filtered_data_by_hour = FilteredDataC02(date=datetime_split[0], time=datetime_split[1], co2_rate=data["co2_rate"])
            filtered_data_by_hour.save()
        pass
