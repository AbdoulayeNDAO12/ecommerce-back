from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name',
                  'image',
                  'more_info',
                  'price',
                  'category',
                  'created',
                  'updated')



