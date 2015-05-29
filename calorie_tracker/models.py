from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Person(User):
    expected_calories = models.IntegerField()

class Meal(models.Model):
    text = models.CharField(max_length=64)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    calories = models.IntegerField()
    user = models.ForeignKey(Person)
