from django.urls import path
from . import api_views

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('', api_views.LastElementsData.as_view()),
]
