import datetime

from django.http import JsonResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.data.data_fetcher import interpolate_data_aux
from app.models import RealDataC02, FilteredDataC02


class LastElementsData(APIView):

    def get(self, request):
        try:
            real_data_tmp = RealDataC02.objects.all()
            filtered_data = FilteredDataC02.objects.all()

            interpolated_data_json_tmp = interpolate_data_aux(filtered_data)
            real_data_json_tmp = [x.to_json() for x in real_data_tmp]
            difference_data_json = [{
                'datetime': x["datetime"],
                'difference': x["co2_rate"] - y["co2_rate"]
            } for x, y in zip(real_data_json_tmp, interpolated_data_json_tmp)]

            json_data_to_send = []
            # Les 3 list json doivent être de la même taille ici
            for i in range(len(real_data_json_tmp)):
                data = {
                    'datetime': real_data_json_tmp[i]["datetime"],
                    'real_co2_rate': real_data_json_tmp[i]["co2_rate"],
                    'interpolated_co2_rate': interpolated_data_json_tmp[i]["co2_rate"],
                    'difference': difference_data_json[i]["difference"],
                }
                json_data_to_send.append(data)
            # Todo -> surement devoir faire un parcours pour établir la moyenne à l'instant T
            #   sur les jours ouvrés et week-end
            return JsonResponse(json_data_to_send, safe=False)
        except ValueError as e:
            return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
