from datetime import datetime as dt

from django.http import JsonResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.data.data_fetcher import interpolate_data_aux
from app.models import RealDataC02, FilteredDataC02


class LastElementsData(APIView):

    @staticmethod
    def calcul_moyenne_jours_ouvre_weekend(real_data_json_tmp, interpolated_data_json_tmp):
        moy_json = []
        nb_data_jours_ouvres = 0
        nb_data_jours_weekend = 0
        current_total_jours_ouvre_real_co2_rate = 0
        current_total_jours_weekend_real_co2_rate = 0
        current_total_jours_ouvre_interpolated_co2_rate = 0
        current_total_jours_weekend_interpolated_co2_rate = 0
        moy_jours_ouvre_real_co2_rate = 0
        moy_weekend_real_co2_rate = 0
        moy_jours_ouvre_interpolated_co2_rate = 0
        moy_weekend_interpolated_co2_rate = 0
        for i in range(len(real_data_json_tmp)):
            if dt.fromtimestamp(real_data_json_tmp[i]["datetime"]).weekday() < 5:
                nb_data_jours_ouvres += 1
                current_total_jours_ouvre_real_co2_rate += real_data_json_tmp[i]["co2_rate"]
                current_total_jours_ouvre_interpolated_co2_rate += interpolated_data_json_tmp[i]["co2_rate"]
                moy_jours_ouvre_real_co2_rate = current_total_jours_ouvre_real_co2_rate / nb_data_jours_ouvres
                moy_jours_ouvre_interpolated_co2_rate = current_total_jours_ouvre_interpolated_co2_rate / nb_data_jours_ouvres
            else:
                nb_data_jours_weekend += 1
                current_total_jours_weekend_real_co2_rate += real_data_json_tmp[i]["co2_rate"]
                current_total_jours_weekend_interpolated_co2_rate += interpolated_data_json_tmp[i]["co2_rate"]
                moy_weekend_real_co2_rate = current_total_jours_weekend_real_co2_rate / nb_data_jours_weekend
                moy_weekend_interpolated_co2_rate = current_total_jours_weekend_interpolated_co2_rate / nb_data_jours_weekend

            data = {
                'nb_data_jours_ouvres': nb_data_jours_ouvres,
                'nb_data_jours_weekend': nb_data_jours_weekend,
                'current_total_jours_ouvre_real_co2_rate': current_total_jours_ouvre_real_co2_rate,
                'current_total_jours_weekend_real_co2_rate': current_total_jours_weekend_real_co2_rate,
                'current_total_jours_ouvre_interpolated_co2_rate': current_total_jours_ouvre_interpolated_co2_rate,
                'current_total_jours_weekend_interpolated_co2_rate': current_total_jours_weekend_interpolated_co2_rate,
                'moy_jours_ouvre_real_co2_rate': moy_jours_ouvre_real_co2_rate,
                'moy_weekend_real_co2_rate': moy_weekend_real_co2_rate,
                'moy_jours_ouvre_interpolated_co2_rate': moy_jours_ouvre_interpolated_co2_rate,
                'moy_weekend_interpolated_co2_rate': moy_weekend_interpolated_co2_rate,
            }
            moy_json.append(data)
        return moy_json

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

            moy_json = self.calcul_moyenne_jours_ouvre_weekend(real_data_json_tmp, interpolated_data_json_tmp)
            json_data_to_send = []
            # Les 4 list json doivent être de la même taille ici
            for i in range(len(real_data_json_tmp)):
                if interpolated_data_json_tmp[i]["co2_rate"] != -1:
                    # data = {
                    #     'datetime': dt.fromtimestamp(real_data_json_tmp[i]["datetime"]).strftime("%Y-%m-%dT%H:%M:%S"),
                    #     'real_co2_rate': real_data_json_tmp[i]["co2_rate"],
                    #     'interpolated_co2_rate': interpolated_data_json_tmp[i]["co2_rate"],
                    #     'difference': difference_data_json[i]["difference"],
                    #     'moy_jours_ouvre_real_co2_rate': moy_json[i]["moy_jours_ouvre_real_co2_rate"],
                    #     'moy_weekend_real_co2_rate': moy_json[i]["moy_weekend_real_co2_rate"],
                    #     'moy_jours_ouvre_interpolated_co2_rate': moy_json[i]["moy_jours_ouvre_interpolated_co2_rate"],
                    #     'moy_weekend_interpolated_co2_rate': moy_json[i]["moy_weekend_interpolated_co2_rate"],
                    # }
                    data = {
                        'dt': dt.fromtimestamp(real_data_json_tmp[i]["datetime"]).strftime("%Y-%m-%dT%H:%M:%S"),
                        # 'dt': real_data_json_tmp[i]["datetime"],
                        'r': real_data_json_tmp[i]["co2_rate"],
                        'i': interpolated_data_json_tmp[i]["co2_rate"],
                        'dif': difference_data_json[i]["difference"],
                        'm_jo_r': round(moy_json[i]["moy_jours_ouvre_real_co2_rate"],2),
                        'm_we_r': round(moy_json[i]["moy_weekend_real_co2_rate"],2),
                        'm_jo_i': round(moy_json[i]["moy_jours_ouvre_interpolated_co2_rate"],2),
                        'm_we_i': round(moy_json[i]["moy_weekend_interpolated_co2_rate"],2),
                    }
                    json_data_to_send.append(data)
            return JsonResponse(json_data_to_send, safe=False)
        except ValueError as e:
            return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
