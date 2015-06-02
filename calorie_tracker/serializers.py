__author__ = 'sameer'

from rest_framework import serializers
from models import Person, Meal

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ('id', 'text', 'date', 'time', 'calories', 'person')

    person = serializers.PrimaryKeyRelatedField(read_only=True)

class PersonSerializer(serializers.ModelSerializer):
    meals = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Person
        fields = ('id', 'username', 'meals')

    username = serializers.ReadOnlyField(source='user.username')