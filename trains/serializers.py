from rest_framework import serializers

from .models import Train, TrainStation


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