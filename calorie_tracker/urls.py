__author__ = 'sameer'

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^meals/$', views.MealList.as_view(), name='meal-list'),
    url(r'^meals/(?P<pk>[0-9]+)/$', views.MealDetail.as_view(), name='meal-detail'),
    url(r'^users/$', views.PersonList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.PersonDetail.as_view(), name='user-detail'),
]
urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]