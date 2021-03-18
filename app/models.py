from django.db import models


class RealDataC02(models.Model):
    datetime = models.FloatField()
    co2_rate = models.IntegerField()

    def __str__(self):
        return "datetime:" + str(self.datetime) + ", co2_rate:" + str(self.co2_rate)

    def to_json(self):
        return {
            "datetime": self.datetime,
            "co2_rate": self.co2_rate
        }


class FilteredDataC02(models.Model):
    datetime = models.FloatField()
    co2_rate = models.IntegerField()

    def __str__(self):
        return "datetime:" + str(self.datetime) + ", co2_rate:" + str(self.co2_rate)

    def to_json(self):
        return {
            "datetime": self.datetime,
            "co2_rate": self.co2_rate
        }