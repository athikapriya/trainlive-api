from rest_framework import serializers

from .models import Train


# =========================================================
# Train Serializers section
# =========================================================
class TrainSerializers(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = [
            "number",
            'name',
            "name_bn",
            "direction",
            "off_day",
            "is_active",
        ]