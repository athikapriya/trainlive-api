from rest_framework import serializers
from django.contrib.gis.geos import Point

from .models import Station


# ==============================================
# StationSerializers section
# ==============================================
class StationSerializer(serializers.ModelSerializer):

    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)

    class Meta:
        model = Station
        fields = [
            "name",
            "name_en",
            "latitude",
            "longitude",
        ]

    def create(self, validated_data):
        latitude = validated_data.pop("latitude")
        longitude = validated_data.pop("longitude")
        validated_data['geom'] = Point(
            longitude,
            latitude,
            srid=4326,
        )
        return Station.objects.create(**validated_data)

    def to_representation(self, instance):
        return {
            "name" : instance.name,
            "name_en" : instance.name_en,
            "latitude" : instance.geom.y if instance.geom else None,
            "longitude" : instance.geom.x if instance.geom else None,
        }