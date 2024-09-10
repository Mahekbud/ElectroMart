from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Category
        fields = '__all__'
        