from datetime import datetime as dt
from typing import List, Dict

from django.http import JsonResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.data.data_fetcher import interpolate_data_aux
from app.models import RealDataC02, FilteredDataC02


class Co2RateData(APIView):

    @staticmethod
    def calcul_moyenne_jours_ouvre_weekend(real_data_json_tmp: List[Dict], interpolated_data_json_tmp: List[Dict]):
        """
        Génère une liste de données de la même taille que celles en entrée
        Cette liste contient les moyennes de C02 à l'instant T pour les jours ouvrés et week end
        :param real_data_json_tmp: Les données réelle sur le C02
        :param interpolated_data_json_tmp: Les données interpolé sur le C02
        :return: Une liste de json avec les informations sur les moyennes de co2 pour les jours ouvrés et les weekend
        """
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
        """
        Répond à la requête Get de l'api
        Les champs ont des noms volontairment court pour réduire la taille des données envoyés
        :param request: Contient les données de la requête get envoyé à l'api
        :return: Une reponse JSON avec comme contenu une list de json au format
        {
            'dt': # Datetime
            'r':  # Donnée C02 réel
            'i':  # Donnée C02 interpolé
            'dif': # Difference entre la donnée réelle et la donnée interpolé
            'm_jo_r': # Moyenne à l'instant T des données C02 réel pour les jours ouvrés
            'm_we_r': # Moyenne à l'instant T des données C02 réel pour les week end
            'm_jo_i': # Moyenne à l'instant T des données C02 interpolé pour les jours ouvrés
            'm_we_i': # Moyenne à l'instant T des données C02 interpolé pour les week end
        }
        """
        try:
            real_data_tmp = RealDataC02.objects.all()
            filtered_data = FilteredDataC02.objects.all()

            filtered_data_json_tmp = [x.to_json() for x in filtered_data]
            interpolated_data_json_tmp = interpolate_data_aux(filtered_data_json_tmp)
            real_data_json_tmp = [x.to_json() for x in real_data_tmp]
            # Pop obligatoire pour avoir des listes de même taille
            real_data_json_tmp.pop()
            difference_data_json = [{
                'datetime': x["datetime"],
                'difference': x["co2_rate"] - y["co2_rate"]
            } for x, y in zip(real_data_json_tmp, interpolated_data_json_tmp)]

            moy_json = self.calcul_moyenne_jours_ouvre_weekend(real_data_json_tmp, interpolated_data_json_tmp)
            json_data_to_send = []
            # Les 4 list json doivent être de la même taille ici
            for i in range(len(real_data_json_tmp)):
                data = {
                    'dt': dt.fromtimestamp(real_data_json_tmp[i]["datetime"]).strftime("%Y-%m-%dT%H:%M:%S"),
                    'r': real_data_json_tmp[i]["co2_rate"],
                    'i': interpolated_data_json_tmp[i]["co2_rate"],
                    'dif': difference_data_json[i]["difference"],
                    'm_jo_r': round(moy_json[i]["moy_jours_ouvre_real_co2_rate"], 2),
                    'm_we_r': round(moy_json[i]["moy_weekend_real_co2_rate"], 2),
                    'm_jo_i': round(moy_json[i]["moy_jours_ouvre_interpolated_co2_rate"], 2),
                    'm_we_i': round(moy_json[i]["moy_weekend_interpolated_co2_rate"], 2),
                }
                json_data_to_send.append(data)
            return JsonResponse(json_data_to_send, safe=False)
        except ValueError as e:
            return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
