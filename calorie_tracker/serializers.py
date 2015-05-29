__author__ = 'sameer'

from rest_framework import serializers
from models import Person, Meal

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ('id', 'text', 'date', 'time', 'calories', 'person')

