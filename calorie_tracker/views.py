from django.shortcuts import render

# Create your views here.

from models import Meal, Person
from datetime import datetime
from serializers import MealSerializer, PersonSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from permissions import IsOwner, CreateOnlyIfNotAuth, AdminOrSelf
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from django.contrib.auth.models import User

class MealList(generics.ListCreateAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = (IsOwner, permissions.IsAuthenticated)

    def get(self, request, *args, **kwargs):
        params = request.GET
        meals = Meal.objects

        if request.user.is_staff:
            if 'person' in params:
                username = params['person']
                person = User.objects.get_by_natural_key(username).person
                meals = meals.filter(person = person)
        else:
            person = request.user.person
            meals = meals.filter(person = person)

        if 'start_time' in params:
            start_time = datetime.strptime(params['start_time'], "%H%M%S").time()
            meals = meals.filter(time__gte = start_time)
        if 'end_time' in params:
            end_time = datetime.strptime(params['end_time'], "%H%M%S").time()
            meals = meals.filter(time__lte = end_time)
        if 'start_date' in params:
            start_date = datetime.strptime(params['start_date'], "%Y%m%d").date()
            meals = meals.filter(date__gte = start_date)
        if 'end_date' in params:
            end_date = datetime.strptime(params['end_date'], "%Y%m%d").date()
            meals = meals.filter(date__lte = end_date)
        serializer = MealSerializer(meals.all(), many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user = self.request.user
        person = User.objects.get_by_natural_key(user.username).person
        serializer.save(person=person)


class MealDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = (permissions.IsAuthenticated,)


class PersonList(generics.ListCreateAPIView):
    permission_classes = (CreateOnlyIfNotAuth,)
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            persons = Person.objects
            serializer = PersonSerializer(persons.all(), many=True)
            return Response(serializer.data)
        else:
            person = Person.objects.get(user = request.user)
            serializer = PersonSerializer(person)
            return Response(serializer.data)

class PersonDetail(generics.RetrieveUpdateAPIView):
    permission_classes = (AdminOrSelf,)
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def put(self, request, *args, **kwargs):
        try:
            person = Person.objects.get(pk=kwargs['pk'])
        except Person.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PersonSerializer(person, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'meals': reverse('meal-list', request=request, format=format)
    })