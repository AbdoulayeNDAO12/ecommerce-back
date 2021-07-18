from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Searchs


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Searchs
        fields = ('searchId',
                  'searchName')



