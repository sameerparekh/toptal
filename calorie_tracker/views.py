from django.shortcuts import render

# Create your views here.

from models import Meal, Person
from datetime import datetime
from serializers import MealSerializer, PersonSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions
from permissions import IsOwnerOrStaff, CreateOnlyIfNotAuth, SuperuserOrSelf
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from django.views.decorators.csrf import ensure_csrf_cookie

class MealList(generics.ListCreateAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = (IsOwnerOrStaff, permissions.IsAuthenticated)

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

        filtered = False
        if 'start_time' in params:
            start_time = datetime.strptime(params['start_time'], "%H%M%S").time()
            meals = meals.filter(time__gte = start_time)
            filtered = True
        if 'end_time' in params:
            end_time = datetime.strptime(params['end_time'], "%H%M%S").time()
            meals = meals.filter(time__lte = end_time)
            filtered = True
        if 'start_date' in params:
            start_date = datetime.strptime(params['start_date'], "%Y%m%d").date()
            meals = meals.filter(date__gte = start_date)
            filtered = True
        if 'end_date' in params:
            end_date = datetime.strptime(params['end_date'], "%Y%m%d").date()
            meals = meals.filter(date__lte = end_date)
            filtered = True

        if not filtered:
            meals = meals.filter(date = datetime.now().date())

        serializer = MealSerializer(meals.all(), many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            person = User.objects.get_by_natural_key(self.request.user.username).person
            serializer.save(person=person)
        else:
            serializer.save()


class MealDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = (IsOwnerOrStaff, permissions.IsAuthenticated)


class PersonList(generics.ListCreateAPIView):
    permission_classes = (CreateOnlyIfNotAuth,)
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            persons = Person.objects
            serializer = PersonSerializer(persons.all(), many=True)
        else:
            person = Person.objects.get(user = request.user)
            serializer = PersonSerializer([person], many=True)

        return Response(serializer.data)

class PersonDetail(generics.RetrieveUpdateAPIView):
    permission_classes = (SuperuserOrSelf,)
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, partial=True, **kwargs)


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'meals': reverse('meal-list', request=request, format=format)
    })

@ensure_csrf_cookie
def html_root(request, format=None):
    return render(request, 'index.html')
