from rest_framework import serializers
from .models import GeneratedImage


class GeneratedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedImage
        fields = ['user', 'image', 'created_at']
