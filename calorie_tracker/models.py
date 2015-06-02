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

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)