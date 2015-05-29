from django.shortcuts import render

# Create your views here.

from models import Meal
from datetime import time, date
from serializers import MealSerializer
from rest_framework import generics
from rest_framework.response import Response

class MealList(generics.ListCreateAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

    def get(self, request, *args, **kwargs):
        params = request.GET

        meals = Meal.objects
        if 'start_time' in params:
            start_time = time.strptime("%H%M%S", params['start_time'])
            meals = meals.filter(time__gte = start_time)
        if 'end_time' in params:
            end_time = time.strptime("%H%M%S", params['end_time'])
            meals = meals.filter(time__lte = end_time)
        if 'start_date' in params:
            start_date = date.strpdate("%Y%M%D", params['start_date'])
            meals = meals.filter(date__gte = start_date)
        if 'end_date' in params:
            end_date = date.strpdate("%Y%M%D", params['end_date'])
            meals = meals.filter(date__lte = end_date)
        serializer = MealSerializer(meals.all(), many=True)
        return Response(serializer.data)


class MealDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
