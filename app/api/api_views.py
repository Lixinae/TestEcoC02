import datetime

from django.http import JsonResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.data.data_fetcher import grab_data_from_api, filter_co2_data_to_one_hour_frequence, \
    interpolate_data_aux


class LastElementsData(APIView):

    def get(self, request):
        try:
            size = 1
            if "size" in request.GET:
                size = int(request.GET["size"])
            # Todo -> Ici récuperer les informations via la BDD et pas via les fonctions
            #   Ici les fonctions ne sont la qu'a titre de test
            # Faire des appels à la BDD
            # Pour avoir les n derniers, faire -> malist[-n:]
            # request.
            real_data_json_tmp = grab_data_from_api("2017-01-01T00:00:00", "2018-12-31T00:00:00")
            real_data_json = [{
                'datetime': x['datetime'],
                'co2_rate': x['co2_rate'],
                'is_week_day': datetime.datetime.strptime(x['datetime'], '%Y-%m-%dT%H:%M:%S').weekday() < 5
            } for x in real_data_json_tmp]
            print(real_data_json[-size:])
            filtered_data = filter_co2_data_to_one_hour_frequence(real_data_json)

            interpolated_data_json_tmp = interpolate_data_aux(filtered_data)
            interpolated_data_json = [{
                'datetime': x['datetime'],
                'co2_rate': x['co2_rate'],
                'is_week_day': datetime.datetime.strptime(x['datetime'], '%Y-%m-%dT%H:%M:%S').weekday() < 5
            } for x in interpolated_data_json_tmp]

            difference_data_json = [{
                'datetime': x["datetime"],
                'is_week_day': x["is_week_day"],
                'difference_abs': abs(x["co2_rate"] - y["co2_rate"])
            } for x, y in zip(real_data_json, interpolated_data_json)]

            json_data = {
                'real_data': real_data_json[-size:],
                'interpolated_data': interpolated_data_json[-size:],
                'difference_data': difference_data_json[-size:],
            }
            return JsonResponse(json_data, safe=False)
        except ValueError as e:
            return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
