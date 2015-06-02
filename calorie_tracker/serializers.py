__author__ = 'sameer'

from rest_framework import serializers
from models import Person, Meal
from django.contrib.auth.models import User

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ('id', 'text', 'date', 'time', 'calories', 'person')

    person = serializers.PrimaryKeyRelatedField(read_only=True)

class PersonSerializer(serializers.ModelSerializer):
    meals = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Person
        fields = ('id', 'expected_calories', 'username', 'email', 'password', 'meals')
        extra_kwargs = {'password': {'write_only': True} }

    username = serializers.CharField(source='user.username', read_only=False)
    email = serializers.CharField(source='user.email', read_only=False)
    password = serializers.CharField(source='user.password', read_only=False)

    def create(self, validated_data):
        username = validated_data['user']['username']
        password = validated_data['user']['password']
        email = validated_data['user']['email']
        user = User.objects.create_user(username, email, password)
        user.save()
        return Person.objects.create(user=user, expected_calories=validated_data['expected_calories'])