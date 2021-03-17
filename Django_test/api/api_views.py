import json

from django.http import HttpResponse, JsonResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class LastElementsData(APIView):

    def get(self, request):
        try:
            print(request)
            # Todo -> Ici récuperer les informations sur les données
            # Pour avoir les n derniers, faire -> malist[:-n]
            # request.
            real_data_json = []
            interpolated_data_json = []
            difference_data_json = [{
                'datetime': x["datetime"],
                'difference_abs': abs(x["co2_rate"] - y["co2_rate"])
            } for x, y in zip(real_data_json, interpolated_data_json)]
            json_data = {
                'real_data': real_data_json,
                'interpolated_data': interpolated_data_json,
                'difference_data': difference_data_json,
            }
            return JsonResponse(json_data, safe=False)
        except ValueError as e:
            return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
