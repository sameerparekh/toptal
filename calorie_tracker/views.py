from django.shortcuts import render

# Create your views here.

from models import *
from datetime import time, date
from serializers import MealSerializer
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class MealList(APIView):
    def get(self, request, format=None):
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

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = MealSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MealDetail(APIView):
    def get_object(self, pk):
        try:
            meal = Meal.objects.get(pk=pk)
        except Meal.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return meal

    def get(self, request, pk, format=None):
        meal = self.get_object(pk)
        serializer = MealSerializer(meal)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        meal = self.get_object(pk)
        data = JSONParser().parse(request)
        serializer = MealSerializer(meal, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        meal = self.get_object(pk)
        meal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
