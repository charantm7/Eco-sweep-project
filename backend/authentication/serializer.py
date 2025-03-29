from rest_framework import serializers
from .models import CleanedPhoto

class CleanedPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CleanedPhoto
        fields = '__all__'