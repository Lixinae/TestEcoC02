import datetime
import json
import requests
from typing import List, Dict, Tuple


def grab_data_from_api(start_time: str, end_time: str) -> Tuple:
    """
    Récupère la data à partir de l'api d'ecoco2
    "http://api-recrutement.ecoco2.com/v1/data/"
    :param start_time: Date de début des données au format "2017-01-01T00:00:00"
    :param end_time: Date de fin des donnéesau format "2017-01-01T00:00:00"
    """
    url = "http://api-recrutement.ecoco2.com/v1/data/"
    payload = {
        "start": convert_date_time_to_timestamp(start_time),
        "end": convert_date_time_to_timestamp(end_time),
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers, params=payload)
    json_data = []
    if response.status_code == 200:
        json_data = response.json()
    return response.status_code, json_data


def filter_by_hour(value: json) -> bool:
    """
    Fonction utilisé dans le filtre
    Vérifie le 2e paramètre du split sur le champ "datetime" et indique si c'est un "00" (heure pleine)
    :param value: Le json sur lequel on veut tester la valeur
    :return: True si c'est l'on a une heure pleine
    """
    if "datetime" not in value:
        return False
    date_splits = value["datetime"].split(":")
    if len(date_splits) < 2:
        return False
    # On sais que le 2e argument sera les minutes, 0 min -> heure pleine
    return date_splits[1] == "00"


def filter_co2_data_to_one_hour_frequence(all_co2_data: List[Dict]) -> List[Dict]:
    """
    Génère une nouvelle liste avec une fréquence par heure à partir des données en entrée
    :param all_co2_data: Toute les données Co2 en entrée avec une fréquence de 30min
    :return: Liste de données avec une fréquence de 30min
    """
    filtered_data = list(filter(filter_by_hour, all_co2_data))
    return filtered_data


def convert_date_time_to_timestamp(date_time: str) -> float:
    """
    Convertis une date du format '%Y-%m-%dT%H:%M:%S' (Année - Mois - Jour T Heures:Minutes:Secondes) vers un timestamp
    :param date_time: La date au format '%Y-%m-%dT%H:%M:%S'
    :return: Le timestamp de la date en entrée
    """
    date_time_obj = datetime.datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%S')
    # On doit rester en UTC pour éviter le bug avec le DST par rapport à la timezone
    return date_time_obj.replace(tzinfo=datetime.timezone.utc).timestamp()


def interpolate_data(current_data: Dict, previous_data: Dict, next_data: Dict) -> float:
    """
    Interpole la donnée current_data_co2_rate à partir des données précédente et suivante
    :param current_data: La donnée actuelle
    :param previous_data: La donnée précédente
    :param next_data: La donnée suivante
    :return: Le co2_rate interpolé à partir des données en entrée
    """
    if ("datetime" not in current_data) or \
            ("datetime" not in previous_data) or \
            ("datetime" not in next_data) or \
            ("co2_rate" not in previous_data) or \
            ("co2_rate" not in next_data):
        return -1
    current_data_time = current_data["datetime"]  # X
    # current_data_co2_rate = current_data["co2_rate"]  # On cherche à calculer cette valeur, Y

    previous_time = previous_data["datetime"]  # X1
    previous_co2_rate = previous_data["co2_rate"]  # Y1

    next_time = next_data["datetime"]  # X2
    next_co2_rate = next_data["co2_rate"]  # Y2
    # y = y1 + ((x – x1) / (x2 - x1) × (y2 - y1))
    co2_rate = previous_co2_rate + (
            (current_data_time - previous_time) / (next_time - previous_time) *
            (next_co2_rate - previous_co2_rate)
    )
    return co2_rate


def interpolate_all_data_from_tmp(interpolated_data_tmp: List[Dict]) -> List[Dict]:
    """
    Calcule toute les données à interpolé à partir de la liste de donnée en entrée
    :param interpolated_data_tmp: Le tableau de données non interpolé, ayant pour valeur -1 s'il y a besoin d'interpolé
    :return: Les données interpolé
    """
    interpolated_data = []
    index = 0
    for data_tmp in interpolated_data_tmp:
        if data_tmp["co2_rate"] == -1 and index + 1 < len(interpolated_data_tmp):
            previous_data = interpolated_data_tmp[index - 1]
            next_data = interpolated_data_tmp[index + 1]
            data_interpolated = {
                'datetime': data_tmp["datetime"],
                'co2_rate': interpolate_data(current_data=data_tmp, previous_data=previous_data, next_data=next_data)
            }
            interpolated_data.append(data_interpolated)
        else:
            interpolated_data.append(data_tmp)
        index += 1
    return interpolated_data


def generate_tmp_interpolated_data(filtered_data: List) -> List[Dict]:
    """
    Génère une liste de données à partir des données filtré
    Indique -1 si la donnée doit être interpolé par la suite
    :param filtered_data: Les données filtré par heure
    :return: La liste de données complète, avec les données à interpolé
    """
    interpolated_data_tmp = []
    i = 0
    for data in filtered_data:
        # data_json = data.to_json()
        interpolated_data_tmp.append(data)
        # On ne peut interpoler que si l'on a la donnée précédente et suivante
        # Donc le dernier élément ne doit pas être ajouté
        if i + 1 < len(filtered_data):
            # On a une liste par heure et on veut rajouter les 30min entre chaque -> +1800
            new_data_to_interpolate = {
                'datetime': data["datetime"] + 1800,
                'co2_rate': -1
            }
            interpolated_data_tmp.append(new_data_to_interpolate)
        i += 1
    return interpolated_data_tmp


# Données en entré filtré par heure
def interpolate_data_aux(filtered_data: List) -> List[Dict]:
    """
    Génère la liste de données à interpolé
    Réalise l'interpolation sur les éléments nécessaire et renvoie la liste des données interpolé
    :param filtered_data: Les données filtré par heure
    :return: La liste des données interpolé
    """
    interpolated_data_tmp = generate_tmp_interpolated_data(filtered_data)
    interpolated_data = interpolate_all_data_from_tmp(interpolated_data_tmp)
    return interpolated_data
