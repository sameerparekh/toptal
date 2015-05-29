from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
from models import *
from datetime import time, date
from serializers import MealSerializer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def meals(request):
    if(request.method == "POST"):
        data = JSONParser().parse(request)
        serializer = MealSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        else:
            return JSONResponse(serializer.errors, status=400)

    elif(request.method == "GET"):
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
        return JSONResponse(serializer.data)

    else:
        return HttpResponseBadRequest("GET, POST, or DELETE only")

def meals_detail(request, pk):
    try:
        meal = Meal.objects.get(pk=pk)
    except Meal.DoesNotExist:
        return HttpResponseNotFound()

    if(request.method == "GET"):
        serializer = MealSerializer(meal)
        return JSONResponse(serializer.data)

    elif(request.method == "PUT"):
        data = JSONParser().parse(request)
        serializer = MealSerializer(meal, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        else:
            return JSONResponse(serializer.errors, status=400)

    elif(request.method == "DELETE"):
        meal.delete()
        return HttpResponse(status=204)