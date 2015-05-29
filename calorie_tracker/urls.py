__author__ = 'sameer'

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = [
    url(r'^meals/$', views.MealList.as_view()),
    url(r'^meals/(?P<pk>[0-9]+)/$', views.MealDetail.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
urlpatterns = format_suffix_patterns(urlpatterns)