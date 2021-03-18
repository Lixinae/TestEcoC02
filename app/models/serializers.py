from rest_framework import serializers
from models import RealDataC02, FilteredDataC02


class RealDataC02Serializer(serializers.ModelSerializer):
    class Meta:
        model = RealDataC02
        fields = ('date', 'co2_rate')
