from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Person(models.Model):
    user = models.OneToOneField(User)
    expected_calories = models.IntegerField(null=True, blank=True)

class Meal(models.Model):
    text = models.CharField(max_length=64, default="")
    date = models.DateField(auto_now_add=True, db_index=True)
    time = models.TimeField(auto_now_add=True, db_index=True)
    calories = models.IntegerField()
    person = models.ForeignKey(Person, related_name='meals')
