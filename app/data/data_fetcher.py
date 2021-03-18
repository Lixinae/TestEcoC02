# from Django_test.models import C02
import datetime
import json
from typing import List
import requests


def grab_data_from_api(start_time, end_time):
    """
    Récupère la data à partir de l'api d'ecoco2
    "http://api-recrutement.ecoco2.com/v1/data/?start_time="
    :param start_time: Date de début des données
    :param end_time: Date de fin des données
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
    json_data = response.json()
    # Pour chaque valeur json dans le tableau renvoyé
    # Créer une entrée dans la BDD

    return json_data


# def fetch_all_data_from_db():
#     all_co2_data = C02.objects.all()
#     return all_co2_data


def filter_by_hour(value: json):
    date_splits = value["datetime"].split(":")
    # On sais que le 2e argument sera les minutes, 0 min -> heure pleine
    return date_splits[1] == "00"


def filter_co2_data_to_one_hour_frequence(all_co2_data: List):
    filtered_data = list(filter(filter_by_hour, all_co2_data))
    return filtered_data


def convert_date_time_to_timestamp(date_time: str):
    date_time_obj = datetime.datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%S')
    # On doit rester en UTC pour éviter le bug avec le DST par rapport à la timezone
    return date_time_obj.replace(tzinfo=datetime.timezone.utc).timestamp()


def interpolate_data(current_data, previous_data, next_data):
    current_data_time = convert_date_time_to_timestamp(current_data["datetime"])  # X
    current_data_co2_rate = current_data["co2_rate"]  # On cherche à calculer cette valeur, Y

    previous_time = convert_date_time_to_timestamp(previous_data["datetime"])  # X1
    previous_co2_rate = previous_data["co2_rate"]  # Y1

    next_time = convert_date_time_to_timestamp(next_data["datetime"])  # X2
    next_co2_rate = next_data["co2_rate"]  # Y2
    # y = y1 + ((x – x1) / (x2 - x1) × (y2 - y1))
    co2_rate = previous_co2_rate + (
            (current_data_time - previous_time) / (next_time - previous_time) *
            (next_co2_rate - previous_co2_rate)
    )
    return co2_rate


def interpolate_all_data_from_tmp(interpolated_data_tmp):
    interpolated_data = []
    index = 0
    for data_tmp in interpolated_data_tmp:
        if data_tmp["co2_rate"] == -1:
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


def generate_tmp_interpolated_data(filtered_data):
    interpolated_data_tmp = []
    i = 0
    for data in filtered_data:
        interpolated_data_tmp.append(data)
        # On ne peut interpoler que si l'on a la donnée précédente et suivante
        # Donc le dernier élément ne doit pas être ajouté
        if i + 1 < len(filtered_data):
            date_splits = data["datetime"].split(":")
            date_splits[1] = "30"
            date_time = ":".join(date_splits)
            new_data_to_interpolate = {
                'datetime': date_time,
                'co2_rate': -1
            }
            interpolated_data_tmp.append(new_data_to_interpolate)
        i += 1
    return interpolated_data_tmp


# Données en entré filtré par heure
def interpolate_data_aux(filtered_data):
    interpolated_data_tmp = generate_tmp_interpolated_data(filtered_data)
    interpolated_data = interpolate_all_data_from_tmp(interpolated_data_tmp)
    return interpolated_data


# Todo -> Tout ce code sera dans une api à terme

co2_data_fetched = grab_data_from_api("2017-01-01T00:00:00", "2019-01-01T00:00:00")
filtered_data = filter_co2_data_to_one_hour_frequence(co2_data_fetched)
interpolated_data = interpolate_data_aux(filtered_data)
data_difference = [{
    'datetime': x["datetime"],
    'difference_abs': abs(x["co2_rate"] - y["co2_rate"])
} for x, y in zip(co2_data_fetched, interpolated_data)]