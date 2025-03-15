from rest_framework import serializers
from .models import PointsConfig

class PointsConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointsConfig
        fields = '__all__'
