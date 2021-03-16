from django.db import models


class C02(models.Model):
    datetime = models.DateField
    co2_rate = models.IntegerField


class Horaire(models.Model):
    datetime = models.DateField
