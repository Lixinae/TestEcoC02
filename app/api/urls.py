from django.urls import path
from . import api_views

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('Get_Co2_Rate_Data/', api_views.LastElementsData.as_view()),
]
