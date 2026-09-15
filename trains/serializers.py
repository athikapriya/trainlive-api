from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from .models import Train, TrainStation



# ==============================================
# StationBriefSerializer section
# ==============================================
class StationBriefSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(allow_null=True)
    name_en = serializers.CharField(allow_null=True)
    latitude = serializers.FloatField(allow_null=True)
    longitude = serializers.FloatField(allow_null=True)


# ==============================================
# TrainStationSerializers section
# ==============================================
class TrainStationSerializers(serializers.ModelSerializer):

    station = serializers.SerializerMethodField()

    class Meta:
        model = TrainStation
        fields = [
            "stop_order",
            "station",
            "scheduled_arrival",
            "scheduled_departure",
        ]

    @extend_schema_field(StationBriefSerializer)
    def get_station(self, obj):
        return {
            "id": obj.station.id,
            "name": obj.station.name,
            "name_en": obj.station.name_en,
            "latitude": obj.station.geom.y if obj.station.geom else None,
            "longitude": obj.station.geom.x if obj.station.geom else None,
        }



# =========================================================
# Train Serializers section
# =========================================================
class TrainSerializers(serializers.ModelSerializer):

    stops = TrainStationSerializers(many=True, read_only=True)

    class Meta:
        model = Train
        fields = [
            "number",
            'name',
            "name_bn",
            "direction",
            "off_day",
            "is_active",
            'stops',
        ]