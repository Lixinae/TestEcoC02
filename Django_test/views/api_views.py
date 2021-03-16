import json

from django.contrib.sites import requests
from django.http import HttpResponse, JsonResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def get_co2_data_from_start_to_end(request):
    try:
        json_data = json.loads(request.body)
        start_time = json_data["start_time"]
        end_time = json_data["end_time"]

        return JsonResponse(safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


# class Co2:
#
#     def get(self, request, start_time, end_time):
#         url = "http://api-recrutement.ecoco2.com/v1/data/"
#         payload = {}
#         files = {}
#         headers = {
#             # 'Authorization': 'Bearer SECRET_KEY',
#             'Content-Type': 'application/json'
#         }
#
#         response = requests.request("GET", url, headers=headers, data=payload, files=files)
#         return Response(response)
#
#     def post(self):
