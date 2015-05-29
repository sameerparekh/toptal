__author__ = 'sameer'

from rest_framework import serializers
from models import Person, Meal

class MealSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    text = serializers.CharField(required=False, allow_blank=True, max_length=64)
    date = serializers.DateField(required=False)
    time = serializers.TimeField(required=False)
    calories = serializers.IntegerField()
    person_id = serializers.IntegerField(required=True)

    def get_person_by_name(self, name):
        person = Person.object.filter(username=name).all()[0]
        return person

    def create(self, validated_data):
        return Meal.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.date = validated_data.get('date', instance.date)
        instance.time = validated_data.get('time', instance.time)
        instance.calories = validated_data.get('calories', instance.calories)
        instance.person_id = validated_data.get('person_id', instance.person_id)
        instance.save()
        return instance
