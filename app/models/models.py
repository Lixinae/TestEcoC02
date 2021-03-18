from django.db import models


class RealDataC02(models.Model):
    date = models.DateField
    time = models.TimeField
    co2_rate = models.IntegerField


class FilteredDataC02(models.Model):
    date = models.DateField
    time = models.TimeField
    co2_rate = models.IntegerField

